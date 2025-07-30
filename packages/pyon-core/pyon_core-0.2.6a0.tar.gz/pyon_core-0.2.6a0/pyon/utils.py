""" Pyon: Python Object Notation - Utils """
# --------------------------------------------------------------------------------------------- #

import os
import random
import string
import importlib

# --------------------------------------------------------------------------------------------- #

MAX_ATTEMPTS = 1000

# --------------------------------------------------------------------------------------------- #

PYON_MIME = "application/vnd.pyon+json"
PYON_EXT = "pyon"

# --------------------------------------------------------------------------------------------- #


class EConst:
    """ Constants used for encoding e decoding data in pyon source. """

    AUX1 = "__aux1__"
    AUX2 = "__aux2__"
    AUX3 = "__aux3__"
    AUX4 = "__aux4__"
    AUX5 = "__aux5__"
    AUX6 = "__aux6__"
    AUX7 = "__aux7__"
    CLASS = "__class__"
    DATA = "__data__"
    DICT = "__dict__"
    TYPE = "__type__"
    FIELDS = "_fields"


# --------------------------------------------------------------------------------------------- #


def is_decode_able(value):
    """ Checks if `value` can be decoded. """

    # 1. ...
    return isinstance(value, dict) and (EConst.TYPE in value)


# --------------------------------------------------------------------------------------------- #


def get_class_name(obj):
    """
    Retrieve the fully qualified class name of an object or class.

    Args:
        obj: The object or class to inspect.

    Returns:
        str: A string representing the fully qualified class name, including the module name.
    """

    # 1. ...
    module, name = None, None

    # 2. ...
    if isinstance(obj, type):
        module, name = f"{obj.__module__}", f"{obj.__qualname__}"

    # 3. ...
    else:
        module, name = f"{obj.__class__.__module__}", f"{obj.__class__.__name__}"

    # 4. ...
    return f"{module}.{name}"


# --------------------------------------------------------------------------------------------- #


def get_class(obj):
    """
    Retrieve the class object referenced by a serialized representation.

    Args:
        obj: A dictionary containing serialized class metadata, including the class name.

    Returns:
        type or None: The class object if it exists and can be imported; otherwise, None.
    """

    # 1. ...
    cls = None
    if isinstance(obj, dict) and (EConst.CLASS in obj):

        # 1.1 ...
        class_name = obj[EConst.CLASS]
        if "." in class_name:

            # 2.1 ...
            try:

                # 3.1 ...
                module_name, class_name = class_name.rsplit(".", 1)
                module = importlib.import_module(module_name)

                # 3.2 ...
                cls = getattr(module, class_name)

            # 2.2 ...
            except (ModuleNotFoundError, AttributeError):
                cls = None

    # 2. ...
    return cls


# --------------------------------------------------------------------------------------------- #


def lstrip(s: str, char: str) -> str:
    """
    Removes all leading `char` characters from the beginning of `s` 
    until the first different character is found.

    Example:
        lstrip_until(",,,hello", ",") -> "hello"
        lstrip_until("///path/to/file", "/") -> "path/to/file"
    """
    if not char or len(char) != 1:
        raise ValueError("char must be a single character")

    # 1. Initialize index
    i = 0

    # 1.1 Iterate until a different character is found
    while i < len(s) and s[i] == char:
        i += 1

    # 2. Return the trimmed string
    return s[i:]


# --------------------------------------------------------------------------------------------- #


def get_mangled_name(obj):
    """
    Returns the Python name-mangled prefix for private attributes of the given object's class.

    Args:
        obj: The object whose class name will be used for mangling.

    Returns:
        str: The mangled name prefix (e.g., '_ClassName__').
    """

    # 1. ...
    mangled_name = type(obj).__name__
    mangled_name = lstrip(mangled_name, '_')

    # 2. ...
    return f"_{mangled_name}__"


# --------------------------------------------------------------------------------------------- #


def generate_unique_filename(
    name: str | None = None,
    extension: str | None = None,
    size: int = 5,
    folder_path: str | None = None
) -> str:
    """
    Generates a unique filename composed of a base name, a random suffix, and an extension.

    Args:
        name (str | None): Base name of the file (can be None).
        extension (str | None): File extension without the dot (can be None).
        size (int): Length of the random alphanumeric suffix (default is 3).
        folder_path (str | None): If provided, ensures filename does not already exist in folder.

    Returns:
        str: A unique filename with the specified structure.
    """

    # 1. Setup base values...
    base = name or "file"
    ext = f".{extension}" if extension else ""
    attempts = 0

    # 2. Loop until unique or max attempts...
    while attempts < MAX_ATTEMPTS:

        # 1.1 Generate suffix...
        suffix = ''.join(random.choices(string.ascii_lowercase + string.digits, k=size))
        filename = f"{base}_{suffix}{ext}"

        # 1.2 Check if unique or skip folder check...
        if not folder_path:
            break

        # 1.3 ...
        file_path = os.path.join(folder_path, filename)
        if not os.path.exists(file_path):
            break

        # 1.3 Count attempts...
        attempts += 1

    # 3. Return result...
    return filename


# --------------------------------------------------------------------------------------------- #
