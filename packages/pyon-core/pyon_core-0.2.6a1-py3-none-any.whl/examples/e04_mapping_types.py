# ----------------------------------------------------------------------------------------- #
""" Example 04: Mapping Types """
# ----------------------------------------------------------------------------------------- #

from dataclasses import dataclass
from collections import defaultdict, ChainMap, Counter
from enum import Enum

# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

# 1. Enum for Testing...
class Color(Enum):
    """ Enum representing basic colors. """
    RED = 1
    GREEN = 2
    BLUE = 3

# ----------------------------------------------------------------------------------------- #

# 2. Dataclass for Testing...
@dataclass
class Person:
    """ Dataclass representing a person. """
    name: str
    age: int

# ----------------------------------------------------------------------------------------- #

# 3. Test Objects...
example_data = {

    # 1.1 Testing mapping types...
    "dict": {
        "x": Person("John", 10),
        "y": Person("Paul", 20),
        "z": Person("Michael", 30),
    },
    "defaultdict": defaultdict(int, a=1, b=2),
    "chainmap": ChainMap(
        {"r": Color.RED, "g": Color.GREEN, "b": Color.BLUE},
        {"w": Person("William", 20), "c": Person("Charles", 25)}
    ),
    "counter": Counter({"x": 10, "y": 20})

}

# ----------------------------------------------------------------------------------------- #

# 4. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Perform encoding and decoding...
    encoded = pyon.encode(value)
    decoded = pyon.decode(encoded)

    # 1.3 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded}")
    print(f" Encoded: {encoded}")
    print('----------------\n')

# ----------------------------------------------------------------------------------------- #
