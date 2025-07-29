# ----------------------------------------------------------------------------------------- #
""" Example 01: Number Types """
# ----------------------------------------------------------------------------------------- #

from decimal import Decimal

# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

# 1. Test Objects...
example_data = {

    # 1.1 Testing numeric types...
    "int": 42,
    "float": 3.14,
    "complex": 2 + 3j,
    "decimal": Decimal("123.456")

}

# ----------------------------------------------------------------------------------------- #

# 2. Iterate over the dictionary, encoding and decoding each item...
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
