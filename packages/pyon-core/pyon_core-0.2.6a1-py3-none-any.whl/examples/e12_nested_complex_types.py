# ----------------------------------------------------------------------------------------- #
""" Example 12: Nested - Complex Types """
# ----------------------------------------------------------------------------------------- #

from dataclasses import dataclass
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
    YELLOW = 4
    ORANGE = 5
    BROWN = 6
    BLACK = 7
    WHITE = 8

# ----------------------------------------------------------------------------------------- #

# 2. Dataclass for Testing...
@dataclass
class Person:
    """ Dataclass representing a person. """

    # 1.1 ...
    name: str
    age: int
    height: float
    is_student: bool
    hobbies: tuple
    favorite_numbers: set
    favorite_colors: list
    pets: dict

    # 1.2 ...
    def __repr__(self):
        return f"({Person}):({self.name}):({self.age})"

    # 1.3 ...
    def __hash__(self):
        return hash(self.__repr__())

# ----------------------------------------------------------------------------------------- #

# 3. Test Class...
class Pet:
    """ Class representing a Pet. """

    # 1.1 ...
    def __init__(self, p_type, name, color):
        self.p_type = p_type
        self.name = name
        self.color = color

    # 1.2 Repr output...
    def __repr__(self):
        return f"({Pet}):({self.p_type}):({self.name}):({self.color})"

# ----------------------------------------------------------------------------------------- #

# 4. Persons...
p1 = Person(
    "Alice", 30, 1.65, False, ("reading", "paiting"), {1, 9}, [Color.RED, Color.YELLOW],
    {
        "cat": [Pet("cat", "Malbeck", Color.ORANGE), Pet("cat", "Yuki", Color.WHITE)],
        "dog": [Pet("dog", "Lync", Color.WHITE), Pet("dog", "Nemo", Color.BROWN)],
    }
)

p2 = Person(
    "Bob", 25, 1.80, True, ("gaming", "cycling"), {7, 13}, [Color.BLACK, Color.WHITE],
    {
        "dog": [Pet("dog", "Zync", Color.BLACK)]
    }
)

p3 = Person(
    "Charlie", 40, 1.75, False, ("hiking", "photography"), {1, 13}, [Color.BLACK, Color.WHITE],
    {"dog": None, "cat": None}
)

# ----------------------------------------------------------------------------------------- #

# 4. Test Objects...
example_data = {

    # 1.1 Tuple, Set...
    "tuple-list": ({p1, p2}),

    # 1.2 List, Tuple, Set...
    "list-tuple-set": [({p1, p2}), ({p3})],

    # 1.3 Dict, List, Tuple, Set...
    "dict-list-tuple-set": {
        "a": [({p1}), ({p2})],
        "b": [({p3})]
    },

    # 1.4 Dict, Dict, Dict, List, Tuple, Set...
    "dict-dict-dict-list-tuple-set": {
        "top": {
            "one": {"a": [({p1, p2})]}
        },
        "down": {
            "three": {"b": [({p3})]}
        }
    }

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
    print('----------------\n')

# ----------------------------------------------------------------------------------------- #
