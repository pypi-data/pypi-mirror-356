# ----------------------------------------------------------------------------------------- #
""" Example 03: Colleciton Types """
# ----------------------------------------------------------------------------------------- #

from collections import deque, namedtuple
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

# 2. Namedtuple for Testing...
XData = namedtuple('XData', ['field1', 'field2'])

# ----------------------------------------------------------------------------------------- #

# 3. Test Objects...
example_data = {

    # 1.1 Testing collection types...
    "list": [1, 2, 3, 4],
    "set": {Color.RED, Color.GREEN, Color.BLUE},
    "frozenset": frozenset([5.1, 6.2, 7.3]),
    "deque": deque(["a", "b", "c"]),
    "tuple": (1, "two", 3.0),
    "namedtuple": XData("value1", 123)

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
