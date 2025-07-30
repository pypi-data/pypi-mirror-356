# --------------------------------------------------------------------------------------------- #
""" Main Fast Tests """
# --------------------------------------------------------------------------------------------- #

import time as t
import logging

# --------------------------------------------------------------------------------------------- #

import pyon

# --------------------------------------------------------------------------------------------- #

from pyon import File

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #

LINE = f"\n\n{'#' * 50}\n\n"

# --------------------------------------------------------------------------------------------- #


def main_01():
    """
    Pipeline de criação de dataset de dealer button.
    """

    # 1. ...
    file_path = 'D:/Desenv/Source/ietsira/Python/PokerIA/data/weights/mlp_weights_rank.pt'
    out_path = 'D:/Desenv/Source/ietsira/Python/PokerIA/tmp/file.pyon'
    unload_path = 'D:/Desenv/Source/ietsira/Python/PokerIA/tmp/mlp_weights_rank.pt'

    # 2. ...
    pyon_file = File(path=file_path, export_mode="data")
    pyon.to_file(pyon_file, out_path)

    # 3. ...
    pyon_new: File = pyon.from_file(out_path) # type: ignore
    unloaded = pyon_new.unload(unload_path)

    # 4. ...
    print("\n01:")
    print("--------------------------------------")
    print(f"Unloaded: {unloaded}")
    print(f"Loaded: {pyon_new.loaded}")
    print(f"Temp: {pyon_new.temp}")
    print(f"Temp Path: {pyon_new._tmp_path}")  # pylint: disable=protected-access
    print("--------------------------------------")

    # 5. ...
    print("\n02:")
    print("--------------------------------------")
    loaded = pyon_new.load()
    print(f"loaded: {loaded}")
    print(f"Loaded: {pyon_new.loaded}")
    print(f"Temp: {pyon_new.temp}")
    print(f"Temp Path: {pyon_new._tmp_path}")  # pylint: disable=protected-access
    print("--------------------------------------")

    # 6. ...
    print("\n03:")
    print("--------------------------------------")
    pyon_new.path = None
    unloaded = pyon_new.unload()
    print(f"Unloaded: {unloaded}")
    print(f"Loaded: {pyon_new.loaded}")
    print(f"Temp: {pyon_new.temp}")
    print(f"Temp Path: {pyon_new._tmp_path}")  # pylint: disable=protected-access
    print("--------------------------------------")

    # 7. ...
    print("\n04:")
    print("--------------------------------------")
    loaded = pyon_new.load()
    print(f"loaded: {loaded}")
    print(f"Loaded: {pyon_new.loaded}")
    print(f"Temp: {pyon_new.temp}")
    print(f"Temp Path: {pyon_new._tmp_path}")  # pylint: disable=protected-access
    print("--------------------------------------\n")

# --------------------------------------------------------------------------------------------- #


if __name__ == "__main__":

    # Init time...
    start = t.time()
    try:

        # . ...
        main_01()

    # Error...
    except (ValueError, TypeError, KeyError) as e:  # Replace with specific exceptions as applicable
        logger.error("Error: %s", str(e))


# --------------------------------------------------------------------------------------------- #
