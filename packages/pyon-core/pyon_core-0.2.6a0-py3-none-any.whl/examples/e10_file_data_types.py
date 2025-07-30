# ----------------------------------------------------------------------------------------- #
""" Example 10: Encoding to File and Decoding from File - Data Types """
# ----------------------------------------------------------------------------------------- #

from datetime import datetime, date, time
from decimal import Decimal
from uuid import uuid4
from collections import deque, defaultdict, ChainMap, namedtuple, Counter
from dataclasses import dataclass
from enum import Enum

# ----------------------------------------------------------------------------------------- #

import os
import hashlib
import bitarray

# ----------------------------------------------------------------------------------------- #

import pandas as pd
import numpy as np

# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

from pyon import File

# ----------------------------------------------------------------------------------------- #

# 1. Enum for Testing...
class Color(Enum):
    """
    Enum representing basic colors.

    Attributes:
        RED: Represents the color red.
        GREEN: Represents the color green.
        BLUE: Represents the color blue.
    """
    RED = 1
    GREEN = 2
    BLUE = 3

# ----------------------------------------------------------------------------------------- #

# 2. Dataclass for Testing...
@dataclass
class Person:
    """
    Dataclass representing a person.

    Attributes:
        name (str): The name of the person.
        age (int): The age of the person.
    """
    name: str
    age: int

    # 1.1 String output...
    def __rep__(self):
        return f"Person: {self.name}, {self.age}"

    # 1.2 Repr output...
    def __repr__(self):
        return f"({Person}):({self.name}):({self.age})"

# ----------------------------------------------------------------------------------------- #

# 3. Test Class...
class Cat:
    """
    Class representing a cat.

    Attributes:
        name (str): The name of the cat.
        age (int): The age of the cat.
    """

    # 1.1 ...
    def __init__(self, name, age):
        self.name = name
        self.age = age

    # 1.2 String output...
    def __str__(self):
        return f"Cat: {self.name}, {self.age}"

    # 1.3 Repr output...
    def __repr__(self):
        return f"({Cat}):({self.name}):({self.age})"

# ----------------------------------------------------------------------------------------- #

# 4. Namedtuple for Testing...
XData = namedtuple('XData', ['field1', 'field2'])

# ----------------------------------------------------------------------------------------- #

# 5. Test Objects...
example_data = {

    # 1.1 Testing basic data types...
    "str": "Hello, World!",
    "int": 42,
    "float": 3.14,
    "NoneType": None,

    # 1.2 Testing boolean types...
    "bool (False)": False,
    "bool (True)": True,

    # 1.3 Testing numeric types...
    "complex": 2 + 3j,
    "decimal": Decimal("123.456"),    

    # 1.4 Testing enumeration...
    "enum": Color.RED,

    # 1.5 Testing date and time types...
    "date": date.today(),
    "datetime": datetime.now(),
    "time": time(14, 30, 15),

    # 1.6 Testing collection types...
    "list": [1, 2, 3, 4],
    "set": {1, 2, 3},
    "frozenset": frozenset([1, 2, 3]),
    "deque": deque(["a", "b", "c"]),
    "tuple": (1, "two", 3.0),
    "namedtuple": XData("value1", 123),

    # 1.7 Testing binary types...
    "bytes": b"hello",
    "bitarray": bitarray.bitarray("1101"),
    "bytearray": bytearray([65, 66, 67]),

    # 1.8 Testing mapping types...
    "dict": {"a": 1, "b": 2, "c": 3},
    "defaultdict": defaultdict(int, a=1, b=2),
    "chainmap": ChainMap({"key1": "value1"}, {"key2": "value2"}),
    "counter": Counter({"x": 10, "y": 20}),

    # 1.9 Testing specialized types...
    "uuid": uuid4(),
    "np.ndarray": np.array([[1, 2, 3], [4, 5, 6]]),
    "pd.DataFrame": pd.DataFrame(
        {"col1": [1, 2], "col2": ["a", "b"]}
    ),

    # 1.10 Testing custom classes...
    "class": Cat("Malbec", 6),
    "dataclass": Person("John", 30),

    # 1.11 Testing files...
    "File": File("./data/img.jpg")

}

# ----------------------------------------------------------------------------------------- #

FILE = "./data.pyon"

# ----------------------------------------------------------------------------------------- #

# 6. Encodes to File and Decodes from File...
pyon.to_file(example_data, FILE)
decoded = pyon.from_file(FILE)

# ----------------------------------------------------------------------------------------- #

# 7. Hashs...
EXAMPLE_HASH = hashlib.sha256(str(example_data).encode()).hexdigest()
DECODED_HASH = hashlib.sha256(str(decoded).encode()).hexdigest()

# 8. Print the results...
print('\n----------------')
print(f"Original Hash: {EXAMPLE_HASH}")
print(f" Decoded Hash: {DECODED_HASH}")
print('----------------\n')

# ----------------------------------------------------------------------------------------- #

# 9. Excludes temp file...
if os.path.exists(FILE):
    os.remove(FILE)

# ----------------------------------------------------------------------------------------- #
