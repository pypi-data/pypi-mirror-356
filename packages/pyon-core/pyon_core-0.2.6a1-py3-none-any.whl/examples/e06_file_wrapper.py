# ----------------------------------------------------------------------------------------- #
""" Example 06: File Wrapper """
# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

from pyon import File

# ----------------------------------------------------------------------------------------- #

FILE_PATH = "./data/img.jpg"

# ----------------------------------------------------------------------------------------- #

# 1. Test Objects...
example_data = {

    # 1.1 File Reference: Does not fetch the data. Just saves filesystem references.
    "File-1": File(FILE_PATH, export_mode="reference"),

    # 1.2 File Data: Fetchs the data and encodes it.
    "File-2": File(FILE_PATH, export_mode="data")

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
