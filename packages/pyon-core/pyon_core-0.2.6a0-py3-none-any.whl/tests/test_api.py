# --------------------------------------------------------------------------------------------- #
""" Tests for Pyon: Encode and Decode """
# --------------------------------------------------------------------------------------------- #

from collections import ChainMap, Counter, deque, defaultdict, namedtuple
from dataclasses import dataclass
from datetime import datetime, date, time
from decimal import Decimal
from enum import Enum
from typing import Literal
from uuid import UUID, uuid4

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray

# --------------------------------------------------------------------------------------------- #

import numpy as np
from numpy._typing._array_like import NDArray
import pandas as pd

# --------------------------------------------------------------------------------------------- #

import pytest
import pyon

# --------------------------------------------------------------------------------------------- #

from pyon import File

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


class ComplexEnum(Enum):
    """Enum with complex values (tuples, dicts) for testing."""
    PAIR = ("pair", 2)
    TRIPLE = ("triple", {"x": 3})
    FULL = ("full", {"a": 2, "b": 3})


# --------------------------------------------------------------------------------------------- #


class _TestClass:
    """ Inner test class """

    def __init__(self):
        self.public = 1
        self._protected = 2
        self.__private = 3  # pylint: disable=unused-private-member


# --------------------------------------------------------------------------------------------- #


class ModelConfig:
    """ A class with post-init logic """

    def __init__(self, name):
        self.name = name
        self._model = None

        # 2.1 ...
        self.__init()

    # 1.2 ...
    def __init(self):
        self.__pyon_post_init__()

    # 1.3 ...
    def __pyon_post_init__(self):
        self._model = f"Loaded model: {self.name}"


# --------------------------------------------------------------------------------------------- #


# Namedtuple for Tests
Named = namedtuple("Named", ["field1", "field2"])


# --------------------------------------------------------------------------------------------- #


class TestPyonEncodeDecode:
    """ Test suite for Pyon's encode and decode functions """

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [bitarray("1101"), None, "invalid", 10, 3.14])

    def test_bitarray(self, value: bitarray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for bitarray. """

        # 1. Default test...
        self._test_default(value, bytearray)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [bytearray(b"hello"), None, "invalid", 10, 3.14])

    def test_bytearray(self, value: bytearray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for bytearray. """

        # 1. Default test...
        self._test_default(value, bytearray)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [b"hello", None, "invalid", 10, 3.14])

    def test_bytes(self, value: None | float | bytes | str | int | float):
        """ Test encoding and decoding for bytes. """

        # 1. Default test...
        self._test_default(value, bytes)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [True, False, None, "invalid", 3.14])

    def test_bool(self, value: None | float | bool | Literal['invalid']):
        """ Test encoding and decoding for boolean values. """

        # 1. Default test...
        self._test_default(value, bool)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [ChainMap({"a": 1}, {"b": 2}), None, "invalid", 10, 3.14])

    def test_chainmap(self, value: ChainMap | None | float | str | int | float):
        """ Test encoding and decoding for ChainMap. """

        # 1. Default test...
        self._test_default(value, ChainMap)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Cat("Malbec", 6), None, "invalid", 10, 3.14])

    def test_class(self, value: Cat | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Class. """

        # 1. Default test...
        self._test_default(value, Cat)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [2 + 3j, None, "invalid", 10, 3.14])

    def test_complex(self, value: complex | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for complex numbers. """

        # 1. Default test...
        self._test_default(value, complex)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Counter({"a": 1, "b": 2}), None, "invalid", 10, 3.14])

    def test_counter(self, value: Counter[str] | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Counter. """

        # 1. Default test...
        self._test_default(value, complex)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Person("Alice", 25), None, "invalid", 10, 3.14])

    def test_dataclass(self, value: Person | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for dataclass. """

        # 1. Default test...
        self._test_default(value, Person)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [date.today(), None, "invalid", 10, 3.14])

    def test_date(self, value: date | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for date. """

        # 1. Default test...
        self._test_default(value, date)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [datetime.now(), None, "invalid", 10, 3.14])

    def test_datetime(self, value: datetime | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for datetime. """

        # 1. Default test...
        self._test_default(value, datetime)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Decimal("123.45"), None, "invalid", 10, 3.14])

    def test_decimal(self, value: Decimal | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for complex numbers. """

        # 1. Default test...
        self._test_default(value, Decimal)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [defaultdict(int, a=1), None, "invalid", 10, 3.14])

    def test_defaultdict(self, value: defaultdict | None | str | int | float):
        """ Test encoding and decoding for defaultdict. """

        # 1. Default test...
        self._test_default(value, defaultdict)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [deque(["a", "b"]), None, "invalid", 10, 3.14])

    def test_deque(self, value: deque[str] | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for deque. """

        # 1. Default test...
        self._test_default(value, deque)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [{"key_a": 1, "key_b": 2}, {"key_a": 'a', "key_b": 'b'}])

    def test_dict(self, value: dict[str, int] | dict[str, str]):
        """ Test encoding and decoding for deque. """

        # 1. Default test...
        self._test_default(value, dict)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Color.RED, None, "invalid", 10, 3.14])

    def test_enum(self, value: None | Color | str | int | float):
        """ Test encoding and decoding for Enum. """

        # 1. Default test...
        self._test_default(value, Enum)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [ComplexEnum.PAIR, ComplexEnum.TRIPLE, ComplexEnum.FULL])
    def test_complex_enum_encoding(self, value: ComplexEnum):
        """
        Tests encoding/decoding for Enums with complex values (tuples, dicts).
        """

        # 1. Prepare...
        encoded = pyon.encode(value)
        decoded = pyon.decode(encoded)

        # 2. Validate...
        assert isinstance(decoded, ComplexEnum)
        assert decoded is value

    # ----------------------------------------------------------------------------------------- #


    @pytest.mark.parametrize(
        "value", [File("./tests/data/img.jpg"), None, "invalid", 10, 3.14]
    )

    def test_file(self, value: File | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for File. """

        # 1. Default test...
        self._test_default(value, File)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [2.72, None, "invalid", 10, False])

    def test_float(self, value: float | None | Literal['invalid'] | Literal[10] | Literal[False]):
        """ Test encoding and decoding for float. """

        # 1. Default test...
        self._test_default(value, float)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [frozenset([1, 2, 3]), None, "invalid", 10, 3.14])

    def test_frozenset(self, value: frozenset | None | str | int | float):
        """ Test encoding and decoding for frozenset. """

        # 1. Default test...
        self._test_default(value, frozenset)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [42, None, "invalid", 10, False])

    def test_int(self, value: None | int | str | int | bool):
        """ Test encoding and decoding for int. """

        # 1. Default test...
        self._test_default(value, int)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [Named("value1", 123), None, "invalid", 10, 3.14])

    def test_namedtuple(self, value: Named | None | str | int | float):
        """ Test encoding and decoding for namedtuple. """

        # 1. Default test...
        self._test_default(value, Named)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [{1, 2, 3}, None, "invalid", 10, 3.14])

    def test_set(self, value: set | None | str | int | float):
        """ Test encoding and decoding for set. """

        # 1. Default test...
        self._test_default(value, set)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", ["Hello World", None, "invalid", 10, 3.14])

    def test_str(self, value: str | None | int | float):
        """ Test encoding and decoding for str. """

        # 1. Default test...
        self._test_default(value, str)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [time(14, 30, 15), None, "invalid", 10, 3.14])

    def test_time(self, value: time | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for time. """

        # 1. Default test...
        self._test_default(value, time)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [File, None, "invalid", 10, 3.14])

    def test_type(self, value: File | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for type. """

        # 1. Default test...
        self._test_default(value, type)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [(1, "two", 3.0), None, "invalid", 10, 3.14])

    def test_tuple(self, value: None | float | Literal[1] | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for tuple. """

        # 1. Default test...
        self._test_default(value, tuple)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize("value", [uuid4(), None, "invalid", 10, 3.14])

    def test_uuid(self, value: UUID | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for uuid. """

        # 1. Default test...
        self._test_default(value, UUID)

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value", [np.array([[1, 2, 3], [4, 5, 6]]), None, "invalid", 10, 3.14]
    )

    def test_ndarray(self, value: NDArray | None | float | Literal['invalid'] | Literal[10]):
        """ Test encoding and decoding for Numpy Array. """

        # 1. Valid case...
        if isinstance(value, np.ndarray):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)

            # 1.3 Asserts: decoded...
            assert np.array_equal(decoded, value)  # type: ignore

        # 2. None, Other...
        else:

            # 1.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value  # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value",
        [

            # 1.1 Standard Index, Standard Columns...
            pd.DataFrame({"col1": [1, 2], "col2": ["a", "b"]}, index=["a", "b"]),

            # 1.2 Range Index, Standard Columns...
            pd.DataFrame({"col1": [1, 2, 3]}, index=pd.RangeIndex(start=10, stop=13, step=1)),

            # 1.3 MultiIndex Index, Standard Columns...
            pd.DataFrame(
                {"col1": [1.0, 2.0, 3.0]},
                index=pd.MultiIndex.from_tuples(
                    [("A", 1), ("A", 2), ("B", 1)],
                    names=["group", "id"]
                )
            ),

            # 1.4 Datetime Index, Standard Columns...
            pd.DataFrame(
                {"col1": [10, 20, 30]},
                index=pd.date_range("2025-01-01", periods=3, freq="D")
            ),

            # 1.5 Period Index, Standard Columns...
            pd.DataFrame(
                {"col1": [100, 200]},
                index=pd.period_range("2024Q1", periods=2, freq="Q")
            ),

            # 1.6 Timedelta Index, Standard Columns...
            pd.DataFrame(
                {"col1": [5, 10]},
                index=pd.to_timedelta(["1 days", "2 days"])
            ),

            # 1.7 Categorical Index, Standard Columns...
            pd.DataFrame(
                {"col1": [42, 84]},
                index=pd.CategoricalIndex(["cat", "dog"], name="animal")
            ),

            # 1.8 Float64 Index, Standard Columns...
            pd.DataFrame(
                {"col1": [0.1, 0.2]},
                index=pd.Index([0.1, 0.2], dtype="float64", name="float_id")
            ),

            # 1.9 Int64 Index, Standard Columns...
            pd.DataFrame(
                {"col1": [10, 20]},
                index=pd.Index([100, 200], dtype="int64", name="int_id")
            ),

            # 1.10 UInt64 Index, Standard Columns...
            pd.DataFrame(
                {"col1": [1, 2]},
                index=pd.Index([10, 20], dtype="uint64", name="uint_id")
            ),

            # 1.11 Standard Index, MultiIndex Columns...
            pd.DataFrame(
                [[22.5, 60, 24.1], [23.0, 55, 23.8]],
                index=["row1", "row2"],
                columns=pd.MultiIndex.from_tuples(
                    [("sensor1", "temp"), ("sensor1", "humidity"), ("sensor2", "temp")],
                    names=["device", "measurement"]
                )
            ),

            # 1.12 Standard Index, CategoricalIndex Columns...
            pd.DataFrame(
                [[1, 2]],
                index=["a"],
                columns=pd.CategoricalIndex(["col1", "col2"], name="categorical_col")
            ),

            # 1.13 MultiIndex Index and MultiIndex Columns...
            pd.DataFrame(
                [[1, 2], [3, 4]],
                index=pd.MultiIndex.from_tuples(
                    [("X", "x1"), ("X", "x2")],
                    names=["sample", "sub"]
                ),
                columns=pd.MultiIndex.from_tuples(
                    [("A", 1), ("A", 2)],
                    names=["group", "measure"]
                )
            ),

            # 1.14 Base Types...
            None, "invalid", 10, 3.14,
        ]
    )
    def test_dataframe(self, value: pd.DataFrame | None | float | Literal['invalid'] | Literal[10]):
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
            assert decoded.equals(value)

        # 2. None, Other...
        else:

            # 2.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value  # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "value",
        [

            # 1.1 Standard Index...
            pd.Series([1.5, 2.0, 3.1], index=["a", "b", "c"], name="standard_series"),

            # 1.2 Range Index...
            pd.Series(
                [100, 200, 300],
                index=pd.RangeIndex(start=0, stop=3, step=1),
                name="range_series",
            ),

            # 1.3 MultiIndex...
            pd.Series(
                [10, 20, 30],
                index=pd.MultiIndex.from_tuples(
                    [("X", 1), ("X", 2), ("Y", 1)],
                    names=["category", "code"]
                ),
                name="multiindex_series"
            ),

            # 1.4 Datetime Index...
            pd.Series(
                [1.1, 1.2, 1.3],
                index=pd.date_range("2024-01-01", periods=3, freq="D"),
                name="datetime_series"
            ),

            # 1.5 Period Index...
            pd.Series(
                [11, 22],
                index=pd.period_range("2024Q1", periods=2, freq="Q"),
                name="period_series"
            ),

            # 1.6 Timedelta Index...
            pd.Series(
                [5, 10],
                index=pd.to_timedelta(["1 days", "2 days"]),
                name="timedelta_series"
            ),

            # 1.7 Categorical Index...
            pd.Series(
                [100, 200],
                index=pd.CategoricalIndex(["low", "high"], name="risk_level"),
                name="categorical_series"
            ),

            # 1.8 Float64 Index...
            pd.Series(
                [0.1, 0.2],
                index=pd.Index([0.1, 0.2], dtype="float64", name="float_id"),
                name="float_series"
            ),

            # 1.9 Int64 Index...
            pd.Series(
                [10, 20],
                index=pd.Index([1, 2], dtype="int64", name="int_id"),
                name="int_series"
            ),

            # 1.10 UInt64 Index...
            pd.Series(
                [99, 100],
                index=pd.Index([11, 12], dtype="uint64", name="uint_id"),
                name="uint_series"
            ),

            # 2.1 Base Types...
            None, "invalid", 42, 3.1415,
        ]
    )
    def test_series(
        self, value: pd.Series | None | float | Literal["invalid"] | Literal[42]
    ):
        """ Test encoding and decoding for Pandas Series. """

        # 1. Valid case...
        if isinstance(value, pd.Series):

            # 1.1 Encode, Decode...
            encoded = pyon.encode(value)
            decoded = pyon.decode(encoded)

            # 1.2 Asserts: encoded...
            assert isinstance(encoded, str)

            # 1.3 Asserts: decoded...
            assert isinstance(decoded, pd.Series)
            assert decoded.equals(value)

        # 2. None, Other...
        else:

            # 2.1 Encode, Decode, Asserts...
            decoded = pyon.decode(pyon.encode(value))
            assert decoded == value # type: ignore

    # ----------------------------------------------------------------------------------------- #

    @pytest.mark.parametrize(
        "enc_protected, enc_private, expected_protected, expected_private",
        [
            (True,  False, 2, None),   # Only protected
            (False, True, None, 3),    # Only private
            (True,  True, 2, 3),       # Both protected and private
        ]
    )
    def test_visibility_options(
        self, enc_protected, enc_private, expected_protected, expected_private
    ):
        """
        Tests encoding/decoding with combinations of `enc_protected` and `enc_private`.
        """

        # 1. Prepare...
        obj = _TestClass()
        encoded = pyon.encode(obj, enc_protected=enc_protected, enc_private=enc_private)
        decoded = pyon.decode(encoded)

        # 2. Validate...
        assert isinstance(decoded, _TestClass)
        assert decoded.public == 1
        assert getattr(decoded, "_protected", None) == expected_protected  # pylint: disable=protected-access
        assert getattr(decoded, "_TestClass__private", None) == expected_private

    # ----------------------------------------------------------------------------------------- #

    def _test_default(self, value, clazz):
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
            if not self._is_builtins(clazz) or isinstance(clazz, dict):
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

    # ----------------------------------------------------------------------------------------- #

    def _is_builtins(self, clazz):
        """ Checks if a class is builtins """

        # 1. Checks...
        return isinstance(clazz, type) and clazz in {int, float, bool, str, type}

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
