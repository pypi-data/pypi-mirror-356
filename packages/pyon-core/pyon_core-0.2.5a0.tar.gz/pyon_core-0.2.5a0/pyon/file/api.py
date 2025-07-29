""" Edo File Wrapper """
# --------------------------------------------------------------------------------------------- #

import base64
import logging
import mimetypes
import os
import shutil
import tempfile

# --------------------------------------------------------------------------------------------- #

from typing import Literal

# --------------------------------------------------------------------------------------------- #

import magic

# --------------------------------------------------------------------------------------------- #

import pyon.utils as ut

# --------------------------------------------------------------------------------------------- #

from pyon.utils import PYON_MIME, PYON_EXT

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #

TEMP_FOLDER = "pyon_file"

# --------------------------------------------------------------------------------------------- #


class File:
    """ File class """

    # ----------------------------------------------------------------------------------------- #

    def __init__(
        self,
        path: str | None = None,
        content: bytes | None = None,
        mime: str | None = None,
        export_mode: Literal["data", "reference"] = "reference"
    ):
        """
        Initializes a new instance of the class.

        Args:
            path (str | None, optional): The file path to be used. Defaults to None.
            content (bytes | None, optional): The file content as bytes. Defaults to None.
            mime (str | None, optional): The MIME type of the file. If not provided,
                it will be determined automatically.
            export_mode (Literal["data", "reference"], optional): Determines how the file
                is exported, either as raw data or as a reference to the filesystem.

        Raises:
            ValueError: If both `path` and `content` are None.
        """

        # 1. ...
        if (path is None) and (content is None):
            raise ValueError("Path or Content must be provided")

        # 2. ...
        self.path = self.__clean_path(path) if path else None
        self.content = content

        # 3. ...
        self.mime = self.__get_mime(mime)
        self.export_mode = export_mode

        # 4. ...
        self._tmp_path = None

    # ----------------------------------------------------------------------------------------- #

    @property
    def size(self) -> str:
        """ Returns the size of the file content """

        # 1. ...
        return File.get_size(len(self))

    # ----------------------------------------------------------------------------------------- #

    @property
    def name(self) -> str:
        """ Returns the file name with extension """

        # 1. ...
        output = ''
        if self.path:

            # 1.1 ...
            output = os.path.basename(self.path)

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    @property
    def extension(self) -> str:
        """ Returns the file extension """
        return self.name.split(".")[-1] if "." in self.name else ''

    # ----------------------------------------------------------------------------------------- #

    @property
    def directory(self) -> str:
        """ Returns the folder where the file is located """

        # 1. ...
        output = ''
        if self.path:

            # 1.1 ...
            output = os.path.dirname(self.path)

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    @property
    def loaded(self) -> bool:
        """ If the content is loaded into memory """

        # 1. ...
        return hasattr(self, "content") and self.content is not None

    # ----------------------------------------------------------------------------------------- #

    @property
    def temp(self) -> bool:
        """ If a temp file """

        # 1. ...
        return hasattr(self, "_tmp_path") and self._tmp_path is not None

    # ----------------------------------------------------------------------------------------- #

    def __len__(self) -> int:
        """ Returns the len of the file content in bytes """

        # 1. ...
        output = 0

        # 2. ...
        if self.content:
            output = len(self.content)

        # 3. ...
        elif self.path:
            output = os.path.getsize(self.path)

        # 4. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __str__(self):

        # 1. ...
        output = f"({self.mime}): ({self.extension}) {self.name} - {self.size}"
        status = self._status()

        # 2. ...
        if status:
            output += f" ({status})"

        # 3. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __repr__(self):

        # 1. ...
        output = {
            "mime": self.mime,
            "extension": self.extension,
            "size": self.size,
            "name": self.name,
            "directory": self.directory,
            "export_mode": self.export_mode,
            "loaded": self.loaded,
            "temp": self.temp
        }

        # 2. ...
        return f"{output}"

    # ----------------------------------------------------------------------------------------- #

    def __lt__(self, other: object) -> bool:
        """
        Returns True if this file is smaller than the other.

        Returns:
            bool: Result of size comparison.
        """

        # 1. Type check...
        if not isinstance(other, File):
            return NotImplemented

        # 2. Compare...
        return len(self) < len(other)

    # ----------------------------------------------------------------------------------------- #

    def __le__(self, other: object) -> bool:
        """
        Returns True if this file is smaller or equal to the other.

        Returns:
            bool: Result of size comparison.
        """

        # 1. Type check...
        if not isinstance(other, File):
            return NotImplemented

        # 2. Compare...
        return len(self) <= len(other)

    # ----------------------------------------------------------------------------------------- #

    def __gt__(self, other: object) -> bool:
        """
        Returns True if this file is bigger than the other.

        Returns:
            bool: Result of size comparison.
        """

        # 1. Type check...
        if not isinstance(other, File):
            return NotImplemented

        # 2. Compare...
        return len(self) > len(other)

    # ----------------------------------------------------------------------------------------- #

    def __ge__(self, other: object) -> bool:
        """
        Returns True if this file is bigger or equal to the other.

        Returns:
            bool: Result of size comparison.
        """

        # 1. Type check...
        if not isinstance(other, File):
            return NotImplemented

        # 2. Compare...
        return len(self) >= len(other)

    # ----------------------------------------------------------------------------------------- #

    def __eq__(self, other: object) -> bool:
        """
        Compares files by identity: path or content.

        Returns:
            bool: True if both files refer to the same logical file.
        """

        # 1. Default result...
        result = False
        if isinstance(other, File):

            # 2.1 Path-based identity...
            if self.path and other.path:
                result = (self.path == other.path)

            # 2.2 Content-based fallback...
            elif self.loaded and other.loaded:
                result = (self.content == other.content)

        # 2. Return result...
        return result

    # ----------------------------------------------------------------------------------------- #

    def to_dict(self, encode: bool = False):
        """ Converts to dictionary. """

        # 1. ...
        output = {
            "path": self.path,
            "mime": self.mime,
            "export_mode": self.export_mode
        }

        # 2. ...
        if self.export_mode == "data":
            output["content"] = self._encode() if encode else self._get_content()

        # 3. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    @classmethod
    def from_dict(cls, data: dict):
        """ Loads from dictionary. """

        # 1. ...
        obj = None
        if data:

            # 1.1 ...
            obj = cls.__new__(cls)

            # 1.2 ...
            obj.path = data.get("path")
            obj.mime = data.get("mime")
            obj.export_mode = data.get("export_mode")

            # 1.3 ...
            obj.content = File._decode_content(data.get("content"))

            # 1.4 ...
            obj._tmp_path = None

        # 2. ...
        return obj

    # ----------------------------------------------------------------------------------------- #

    def load(self) -> bool:
        """
        Loads the content of the file at the specified path into memory if not already loaded.

        Returns:
            bool: True if the content is successfully loaded or already present, False otherwise.
        """

        # 1. ...
        if not self.content:
            self.content = self._get_content()

            # 1.1 ...
            if self.temp and self.content:
                self.__clean_tmp()

        # 2. ...
        return self.content is not None

    # ----------------------------------------------------------------------------------------- #

    def unload(self, file_path: str | None = None, update: bool = False) -> bool:
        """
        Unload the current content, optionally writing it to a specified file path.

        If content exists, attempts to write it to:
            - the provided file path or,
            - the object's current path or,
            - a temporary location.
        
        Args:
            file_path (str | None, optional): The file path to write the content to. If None,
            uses the object's current path or a temporary file.
            update (bool, optional): If True, overwrites an existing file at the target path.
        
        Returns:
            bool: True if the content was successfully unloaded (i.e., self.content is None), 
            False otherwise.

        Notes:
            After a successful write, the content is cleared from memory.
            If written to a new `file_path` updates the file `self.path`.
        """

        # 1. ...
        if self.content:
            done = False

            # 1.1 ...
            file_path = self.__clean_path(file_path)
            if file_path:

                # 2.1 ...
                if self.write(outpath=file_path):

                    # 3.1 ...
                    self.path = file_path
                    done = True

            # 1.2 ...
            elif self.path:

                # 2.1 ...
                if update or not os.path.isfile(self.path):
                    done = self.write()

                # 2.2 ...
                else:
                    done = True

            # 1.3 ...
            else:

                # 2.1 ...
                if update or not (self._tmp_path and os.path.isfile(self._tmp_path)):
                    done = self._write_temp()

                # 2.2 ...
                else:
                    done = True

            # 1.4 ...
            if done:
                self.content = None

        # 2. ...
        return self.content is None

    # ----------------------------------------------------------------------------------------- #

    def write(self, outpath: str | None = None, verbose: bool = False) -> bool:
        """
        Writes the file content to disk.
            - If 'content' is available, it writes the content to 'outpath'.
            - If 'content' is not available but 'filepath' is, 
                it copies the file from 'filepath' to 'outpath'.
        """

        # 1. ...
        output = False

        # 2. ...
        path: str = (
            outpath.strip()
            if isinstance(outpath, str)
            else (self.path.strip() if self.path else "")
        )

        # 3. ...
        if len(path) > 0:
            check = False

            # 1.1 ...
            out_dir = os.path.dirname(path)
            file_name = self._get_file_name()

            # 1.2 ...
            if not os.path.exists(out_dir):
                os.makedirs(out_dir, exist_ok=True)

            # 1.3 ...
            if os.path.isdir(path):
                path = self.__clean_path(os.path.join(path, file_name)) # type: ignore

            # 1.4 ...
            if self.content:

                # 2.1 ...
                with open(path, 'wb') as f:
                    f.write(self.content)

                # 2.2 ...
                check = True

            # 1.5 ...
            elif self.path and (path != self.path) and os.path.exists(self.path):

                # 1.1 ...
                if path != self.path:
                    shutil.copy(self.path, path)

                    # 2.1 ...
                    check = True

            # 1.6 ...
            else:
                raise FileNotFoundError(f"Source file not found: {self.path}")

            # 1.7 ...
            if verbose:
                logger.info("File.write(): data saved at %s", path)

            # 1.8 ...
            if check:
                output = os.path.isfile(path)

        # 4. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _write_temp(self, extension: str | None = None) -> bool:
        """
        Writes the current file content to a temporary file with an optional extension.
        This method performs the following steps:
            1. Cleans up any existing temporary files.
            2. Creates a new temporary directory.
            3. Generates a file name with the specified or default extension.
            4. Constructs the full path for the temporary file.
            5. Writes the file content to the temporary file.
            6. Stores the path as `_tmp_path` for later use.
        
        Args:
            extension (str | None): Optional file extension to use for the temporary file.
                If None, a default extension is used.
        
        Returns:
            bool: True if the file was successfully written to the temp location, False otherwise.
        """

        # 1. Output...
        output = False
        if self.__clean_tmp():

            # 1.1 Creates temporary directory...
            tmp_dir = tempfile.mkdtemp(dir=self.__get_temp_dir())
            file_name = self._get_file_name(extension=self.__get_temp_extension(extension))

            # 1.2 Builds full output path...
            tmp_path = self.__clean_path(os.path.join(tmp_dir, file_name))

            # 1.3 Writes the file content...
            if self.write(tmp_path):

                # 2.1 ...
                self._tmp_path = tmp_path
                output = True

        # 2. Returns final path...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _get_content(self) -> bytes | None:
        """
        Returns the file content as bytes.
        """

        # 1. ...
        output = None

        # 2. ...
        if self.content:
            output = self.content

        # 3. ...
        else:
            load_path = None

            # 1.1 ...
            if self._tmp_path and os.path.isfile(self._tmp_path):
                load_path = self._tmp_path

            # 1.2 ...
            elif self.path and os.path.isfile(self.path):
                load_path = self.path

            # 1.3 ...
            if load_path:

                # 2.1 ...
                with open(load_path, 'rb') as file:
                    output = file.read()

        # 4. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _status(self) -> str:
        """ Content loaded or not; if temp file or not """

        # 1. ...
        status = []

        # 2. ...
        if self.loaded:
            status.append("memory")

        # 3. ...
        if self.path and os.path.isfile(self.path):
            status.append("filesystem")

        # 4. ...
        if self.temp:
            status.append("temp")

        # 5. ...
        return ', '.join(status) if status else ""

    # ----------------------------------------------------------------------------------------- #

    def _get_file_name(self, extension: str = 'tmp'):
        """ 
        Returns the filename if exists, else creates one.
        """

        # 1. ...
        return (
            self.name
            if self.name
            else ut.generate_unique_filename(extension=extension, folder_path=self.path)
        )

    # ----------------------------------------------------------------------------------------- #

    def _encode(self) -> str | None:
        """ Encodes the content. """

        # 1. ...
        encoded_content = None
        if (self.export_mode == "data") or (not self.path and self.content):

            # 1.1 ...
            encoded_content = File._encode_content(self._get_content())

        # 2. ...
        return encoded_content

    # ----------------------------------------------------------------------------------------- #

    def __get_mime(self, mime: str | None) -> str:
        """ Returns the mime value """

        # 1. ...
        output = mime.strip() if mime else ''
        if not output:

            # 1.1 ...
            if self.path:

                # 2.1 ...
                if self.extension == PYON_EXT:
                    output = PYON_MIME

                # 2.2 ...
                else:
                    output = File.get_mime_from_path(self.path)

            # 1.2 ...
            if not output and self.content:
                output = File.get_mime_from_content(self.content)

            # 1.3 ...
            if not output and self.name:
                output = File.get_mime_from_name(self.name)

            # 1.4 ...
            if not output:
                output = "application/octet-stream"

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __clean_path(self, path: str | None) -> str:
        """
        Converts the given file path to a normalized string with forward slashes.
        Args:
            path (str): The input file path to normalize.
        Returns:
            str: The normalized file path.
        """

        # 1. ...
        output = ''

        # 2. ...
        if path:
            output = str(path).strip().replace("\\", "/")

        # 3. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __clean_tmp(self) -> bool:
        """
        Deletes the temporary file specified by self._tmp_path, if it exists.
        
        Returns:
            bool: True if the file was successfully deleted or does not exist, False otherwise.
        
        Logs:
            An error message if the file could not be deleted due to an OSError.
        """

        # 1. ...
        clean = True
        if self._tmp_path:

            # 1.1 ...
            clean = False
            try:

                # 2.1 ...
                path = self.__clean_path(self._tmp_path)
                if path:

                    # 3.1 ...
                    if os.path.isfile(path):

                        # 4.1 Remove temp file...
                        os.remove(path)
                        clean = True

                        # 4.2 Remove empty folder...
                        folder = os.path.dirname(path)
                        if os.path.isdir(folder) and not os.listdir(folder):

                            # 5.1 ...
                            os.rmdir(folder)

                    # 3.2 ...
                    else:
                        clean = True

            # 1.2 ...
            except OSError as e:
                logger.error("Error deleting temp file '%s': %s", path, e)

        # 2. ...
        if clean and self._tmp_path:
            self._tmp_path = None

        # 3. ...
        return clean

    # ----------------------------------------------------------------------------------------- #

    def __get_temp_extension(self, value: str | None) -> str:
        """
        Returns a normalized file extension based on the provided value.
        If a value is given, it is stripped of whitespace and converted to lowercase.
        If no value is provided, the method falls to the instance's `self.extension` attribute.
        If `self.extension` is also not set or empty, it defaults to 'tmp'.
        
        Args:
            value (str | None): The file extension to normalize, or None.
        
        Returns:
            str: The normalized file extension.
        """

        # 1. ...
        ext = value.strip().lower() if value else None
        if not ext:

            # 1.1 ...
            ext = self.extension
            if not ext:

                # 2.1 ...
                ext = 'tmp'

        # 2. ...
        return ext

    # ----------------------------------------------------------------------------------------- #

    def __get_temp_dir(self) -> str:
        """
        Returns the path to a temp directory for 'pyon-file', creating it if needed.
        Uses the system's temp dir as base and ensures 'pyon-file' subdir exists.
        
        Returns:
            str: Absolute path to the 'pyon-file' temp directory.
        """

        # 1. ...
        path = os.path.join(tempfile.gettempdir(), TEMP_FOLDER)
        os.makedirs(path, exist_ok=True)

        # 2. ...
        return path

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def get_mime_from_name(filename: str):
        """
        Returns the mime of a filename.
        """

        # 1. ...
        return mimetypes.guess_type(filename)[0] or "application/octet-stream"

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def get_mime_from_path(filepath: str):
        """
        Returns the mime of a filepath.
        """

        # 1. ...
        mime = magic.Magic(mime=True)
        return mime.from_file(filepath)

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def get_mime_from_content(content: bytes):
        """
        Returns the mime of the content.
        """

        # 1. ...
        mime = magic.Magic(mime=True)
        return mime.from_buffer(content)

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def get_size(bytes_size: int) -> str:
        """
        Takes the size of a file in bytes and returns a formatted string
        with the appropriate size unit (KB, MB, GB, etc.).
        """

        # 1. ...
        output = ''
        if isinstance(bytes_size, int) and (bytes_size >= 0):

            # 1.1 Units...
            units = ["bytes", "KB", "MB", "GB", "TB", "PB", "EB", "ZB", "YB"]
            unit_index = 0

            # 1.2 Determine which unit to use...
            while (bytes_size >= 1024) and (unit_index < len(units) - 1): # type: ignore

                # 2.1 ...
                bytes_size /= 1024.0 # type: ignore
                unit_index += 1

            # 1.3 Formats...
            output = f"{bytes_size:.1f} {units[unit_index]}"

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def _encode_content(content: bytes | None) -> str | None:
        """ Encodes the content. """

        # 1. ...
        encoded_content = None
        if content:

            # 1.1 ...
            encoded_content = base64.b64encode(content).decode('utf-8')

        # 2. ...
        return encoded_content

    # ----------------------------------------------------------------------------------------- #

    @staticmethod
    def _decode_content(content: str | bytes | None) -> bytes | None:
        """ Decodes the content. """

        # 1. ...
        decoded_content = None

        # 2. ...
        if isinstance(content, bytes):
            decoded_content = content

        # 3. ...
        elif isinstance(content, str):
            decoded_content = base64.b64decode(content)

        # 4. ...
        return decoded_content

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
