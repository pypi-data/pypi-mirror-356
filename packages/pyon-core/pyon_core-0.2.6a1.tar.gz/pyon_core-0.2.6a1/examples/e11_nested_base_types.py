# ----------------------------------------------------------------------------------------- #
""" Example 11: Nested - Base Types """
# ----------------------------------------------------------------------------------------- #

import pyon

# ----------------------------------------------------------------------------------------- #

# 1. Test Objects...
example_data = {

    # 1.1 Tuple, Set...
    "tuple-set-1": ({"abc", "def"}),
    "tuple-set-2": ({1, 2}),
    "tuple-set-3": ({1.1, 2.2}),
    "tuple-set-4": ({True, False}),

    # 1.2 List, Tuple, Set...
    "list-tuple-set-1": [({"abc", "def"}), ({1, 2}), ({True, False})],
    "list-tuple-set-2": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})],

    # 1.3 Dict, List, Tuple, Set...
    "dict-list-tuple-set": {
        "a": [({"abc", "def"}), ({1, 2}), ({True, False})],
        "b": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})],
    },

    # 1.4 Dict, Dict, Dict, List, Tuple, Set...
    "dict-dict-dict-list-tuple-set": {
        "top": {
            "one": {"a": [({"abc", "def"}), ({1, 2}), ({True, False})]},
            "two": {"b": [({"ghi", "jkl"}), ({3.0, 4.0}), ({True, False})]}
        },
        "down": {
            "three": {"c": [({"mno", "pqr"}), ({3, 4}), ({True, False})]},
            "four": {"d": [({"stu", "vwx"}), ({5.0, 6.0}), ({True, False})]}
        }
    }

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
    print('----------------\n')

# ----------------------------------------------------------------------------------------- #
