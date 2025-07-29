""" Pyon: Python Object Notation - Public Interface """
# --------------------------------------------------------------------------------------------- #

import logging
import os

# --------------------------------------------------------------------------------------------- #

from .encoder import PyonEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


def encode(obj, enc_protected: bool = False, enc_private: bool = False) -> str | None:
    """Encodes a Python object into a Pyon-formatted string.

    Args:
        obj: The Python object to encode.
        enc_protected (bool): Whether to encode protected attributes.
        enc_private (bool): Whether to encode private attributes.

    Returns:
        str or None: The encoded Pyon string, or None if obj is None.
    """

    # 1. ...
    output = None
    if obj is not None:

        # 1.1 ...
        encoder = PyonEncoder(enc_protected=enc_protected, enc_private=enc_private)
        output = encoder.encode_str(obj)

    # 2. ...
    return output


# --------------------------------------------------------------------------------------------- #


def decode(pyon_str: str | None):
    """
    Decodes a Pyon-formatted string into a Python object.

    Args:
        pyon_str (str | None): The Pyon string to decode.

    Returns:
        The decoded Python object, or None if pyon_str is None.
    """

    # 1. ...
    output = None
    if pyon_str is not None:

        # 1.1 ...
        encoder = PyonEncoder()
        output = encoder.decode_str(pyon_str)

    # 2. ...
    return output


# --------------------------------------------------------------------------------------------- #


def to_file(
    obj,
    file_path: str = "./data.pyon",
    enc_protected: bool = False,
    enc_private: bool = False,
    verbose: bool = True,
):
    """ Saves to file """

    # 1. ...
    pyon_text = encode(obj, enc_protected=enc_protected, enc_private=enc_private)

    # 2. ...
    if ((pyon_text is not None) and (len(pyon_text) > 0) and file_path
        and file_path.endswith(".pyon")):

        # 1.1 ...
        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        # 1.2 ...
        with open(file_path, "w", encoding="utf-8") as file:
            file.write(pyon_text)

        # 1.3 ...
        if verbose:
            logger.info("Data saved at %s", file_path)

    # 3. ...
    else:
        raise ValueError(f"Not a valid pyon output file: '{file_path}'")

    # 4. ...
    return pyon_text


# --------------------------------------------------------------------------------------------- #


def from_file(file_path: str):
    """
    Loads and decodes a Pyon-formatted file into a Python object.

    Args:
        file_path (str): The path to the Pyon file.

    Returns:
        The decoded Python object, or None if the file does not exist or is invalid.
    """

    # 1. ...
    pyon_str = None
    if os.path.isfile(file_path):

        # 1.1. ...
        with open(file=file_path, mode="r", encoding="utf-8") as file:
            pyon_str = file.read()

    # 2. ...
    return decode(pyon_str)


# --------------------------------------------------------------------------------------------- #
