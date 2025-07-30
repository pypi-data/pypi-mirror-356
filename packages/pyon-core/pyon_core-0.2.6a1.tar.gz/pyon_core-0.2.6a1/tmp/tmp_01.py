# --------------------------------------------------------------------------------------------- #
""" Main Tests Module """
# --------------------------------------------------------------------------------------------- #

import time as t
import logging
import pandas as pd

# --------------------------------------------------------------------------------------------- #

from collections import ChainMap, Counter, deque, defaultdict, namedtuple
from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from uuid import UUID, uuid4

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray

# --------------------------------------------------------------------------------------------- #

import numpy as np
import pandas as pd

# --------------------------------------------------------------------------------------------- #

import pytest
import pyon

# --------------------------------------------------------------------------------------------- #

from pyon import File

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


# Test Enums
class Color(Enum):
    """ For Enum Test """
    RED = 1
    GREEN = 2
    BLUE = 3


# --------------------------------------------------------------------------------------------- #


# Test Dataclasses
@dataclass
class Person:
    """ For Dataclass Test """
    name: str
    age: int


# --------------------------------------------------------------------------------------------- #


# Test Class
class Cat:
    """ For Dataclass Test """
    name: str
    age: int
    def __init__(self, name, age):
        self.name = name
        self.age = age


# --------------------------------------------------------------------------------------------- #


class ___TestClass:
    """ Inner test class """

    # 1.1 ...
    def __init__(self):
        self.public = 1
        self._protected = 2
        self.__private = 3  # pylint: disable=unused-private-member


# --------------------------------------------------------------------------------------------- #


def test_visibility_options(
        enc_protected, enc_private, expected_protected, expected_private
    ):
    """
    Tests encoding/decoding with combinations of `enc_protected` and `enc_private`.
    """

    # 1. Prepare...
    obj = ___TestClass()
    encoded = pyon.encode(obj, enc_protected=enc_protected, enc_private=enc_private)
    decoded = pyon.decode(encoded)

    # 2. Validate...
    assert isinstance(decoded, ___TestClass)
    assert decoded.public == 1
    assert getattr(decoded, "_protected", None) == expected_protected  # pylint: disable=protected-access
    assert getattr(decoded, "_TestClass__private", None) == expected_private


# --------------------------------------------------------------------------------------------- #

def test_dataframe(value):
    """ Test encoding and decoding for Pandas Dataframe. """

    # 1. Valid case...
    if isinstance(value, pd.DataFrame):

        # 1.1 Encode, Decode...
        encoded = pyon.encode(value)
        decoded = pyon.decode(encoded)

        # 1.2 Asserts: encoded...
        assert isinstance(encoded, str)

        # 1.3 Asserts: decoded...
        assert isinstance(decoded, pd.DataFrame)
        print(value.head())
        print(decoded.head())
        assert decoded.equals(value)

    # 2. None, Other...
    else:

        # 1.1 Encode, Decode, Asserts...
        decoded = pyon.decode(pyon.encode(value))
        assert decoded == value

# --------------------------------------------------------------------------------------------- #

def test_dataframe_verbose(value, label="DataFrame"):
    """ Verbose test for encoding and decoding Pandas DataFrame (for use in main/debug). """

    print(f"\n[TEST] Starting test for: {label}")

    # 1. Valid case...
    if isinstance(value, pd.DataFrame):

        try:
            # 1.1 Encode, Decode...
            print("  - Encoding...")
            encoded = pyon.encode(value)

            print("  - Decoding...")
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)
            print("  - Encoded output is valid JSON string.")

            # 1.3 Asserts: decoded...
            assert isinstance(decoded, pd.DataFrame)
            print("  - Decoded output is a valid DataFrame.")

            assert decoded.equals(value)
            print("  - Decoded DataFrame matches original ✅")

        except Exception as e:
            print(f"  [ERROR] Test failed for: {label}")
            print(f"  Reason: {type(e).__name__}: {e}")
            print("  Original value:")
            print(value)

    # 2. None, Other...
    else:
        try:
            # 2.1 Encode, Decode, Asserts...
            print("  - Encoding non-DataFrame value...")
            encoded = pyon.encode(value)

            print("  - Decoding...")
            decoded = pyon.decode(encoded)

            assert decoded == value
            print("  - Decoded value matches original ✅")

        except Exception as e:
            print(f"  [ERROR] Test failed for: {label}")
            print(f"  Reason: {type(e).__name__}: {e}")
            print("  Original value:")
            print(value)

# --------------------------------------------------------------------------------------------- #


def test_class(value):
    """ Test encoding and decoding for Class. """

    # 1. Default test...
    _test_default(value, Cat)

# ----------------------------------------------------------------------------------------- #

def test_dataclass(value):
    """ Test encoding and decoding for dataclass. """

    # 1. Default test...
    _test_default(value, Person)

# ----------------------------------------------------------------------------------------- #

def _test_default(value, clazz):
    """ Test encoding and decoding for complex numbers. """

    # 1. Valid case...
    if isinstance(clazz, type) and isinstance(value, clazz):

        # 1.1 Encode, Decode...
        encoded = pyon.encode(value)
        decoded = pyon.decode(encoded)

        # 1.2 Asserts: encoded...
        assert encoded != value
        assert isinstance(encoded, str)

        # 1.3 If not builtins, checks name in type...
        if not _is_builtins(clazz) or isinstance(clazz, dict):
            assert clazz.__name__.lower() in encoded.lower()

        # 1.4 Asserts: decoded...
        if not (hasattr(decoded, "__dict__") and isinstance(decoded.__dict__, dict)):
            assert decoded == value

        # 1.5 Asserts: decode dict...
        elif hasattr(value, "__dict__") and isinstance(value.__dict__, dict):
            for key, val in value.__dict__.items():

                # 3.1 Both must have the same key and value...
                assert key in decoded.__dict__
                assert decoded.__dict__[key] == val

        # 1.6 Fails...
        else:
            pytest.fail(
                (
                    f"Fail. Expected: {clazz}. "
                    f"Value: {type(value)}. "
                    f"Result: {type(decoded)}."
                )
            )

    # 2. None, Other...
    else:

        # 1.1 Encode, Decode, Asserts...
        decoded = pyon.decode(pyon.encode(value))
        assert decoded == value

# --------------------------------------------------------------------------------------------- #

def _is_builtins(clazz):
    """ Checks if a class is builtins """

    # 1. Checks...
    return isinstance(clazz, type) and clazz in {int, float, bool, str, type}

# --------------------------------------------------------------------------------------------- #

def main01():
    """ Main Method """

    test_visibility_options(
        enc_protected=True,
        enc_private=False,
        expected_protected=2,
        expected_private=None
    )

    print("DONE!")

# --------------------------------------------------------------------------------------------- #



if __name__ == "__main__":

    # Init time...
    start = t.time()
    try:

        # . ...
        main01()

    # Error...
    except Exception as e:  # pylint: disable=W0718
        logger.error("Error: %s", e)


# --------------------------------------------------------------------------------------------- #
