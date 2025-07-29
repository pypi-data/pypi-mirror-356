# ----------------------------------------------------------------------------------------- #
""" Example 09: Encoding to File and Decoding from File - Collections """
# ----------------------------------------------------------------------------------------- #

from collections import deque, namedtuple
from enum import Enum

# ----------------------------------------------------------------------------------------- #

import os
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

FILE = "./data.pyon"

# ----------------------------------------------------------------------------------------- #

# 4. Encodes to File and Decodes from File...
pyon.to_file(example_data, FILE)
decoded = pyon.from_file(FILE)

# ----------------------------------------------------------------------------------------- #

# 5. Iterate over the dictionary, encoding and decoding each item...
for key, value in example_data.items():

    # 1.1 Display the type...
    print('\n----------------')
    print(f"Type: {key}\n")

    # 1.2 Print the results...
    print(f"Original: {value}")
    print(f" Decoded: {decoded[key]}")
    print('----------------\n')

# ----------------------------------------------------------------------------------------- #

# 6. Excludes temp file...
if os.path.exists(FILE):
    os.remove(FILE)

# ----------------------------------------------------------------------------------------- #
