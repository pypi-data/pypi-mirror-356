# ----------------------------------------------------------------------------------------- #
""" Example 02: Custom Types """
# ----------------------------------------------------------------------------------------- #

from dataclasses import dataclass
from enum import Enum

# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

# 1. Enum for Testing...
class Color(Enum):
    """
    Enum representing basic cat colors.
    """
    BLACK = 1
    WHITE = 2
    BROWN = 3
    ORANGE = 3

# ----------------------------------------------------------------------------------------- #

# 2. Test Class...
class Cat:
    """
    Class representing a cat.
    """

    # 1.1 ...
    def __init__(self, name, color):
        self.name = name
        self.color = color

    # 1.2 String output...
    def __str__(self):
        return f"Cat: {self.name}, {self.color}"

    # 1.3 Repr output...
    def __repr__(self):
        return f"({Cat}):({self.name}):({self.color})"

# ----------------------------------------------------------------------------------------- #

# 3. Dataclass for Testing...
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

# ----------------------------------------------------------------------------------------- #

# 4. Test Objects...
example_data = {

    # 1.1 Testing enumeration...
    "enum": Color.BLACK,

    # 1.2 Testing custom classes...
    "class": Cat("Malbec", Color.ORANGE),
    "dataclass": Person("John", 30)

}

# ----------------------------------------------------------------------------------------- #

# 5. Iterate over the dictionary, encoding and decoding each item...
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
