# --------------------------------------------------------------------------------------------- #
""" Pyon: Mapping Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from dataclasses import is_dataclass
from enum import Enum

# --------------------------------------------------------------------------------------------- #

from ..supported_types import SupportedTypes
from ..utils import EConst

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

from .base_encoder import BaseEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class MapEnc(BaseEncoder):
    """ Mapping Encoder """

    # ----------------------------------------------------------------------------------------- #

    def __init__(self, encoder, enc_protected: bool = False, enc_private: bool = False):
        super().__init__(encoder)

        # 1. ...
        self.enc_protected = enc_protected
        self.enc_private = enc_private

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. ...
        encoded = None
        if self.is_encode(value):

            # 1.1 Enum...
            if isinstance(value, Enum):
                encoded = self._encode_enum(value)

            # 1.2 Dict, Class, Dataclass...
            else:
                encoded = self._encode_dict(value)

        # 2. ...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode(self, value):
        """ Decodes the value """

        # 1. ...
        decoded = None

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Date...
            if _type == SupportedTypes.ENUM.value:
                decoded = self._decode_enum(value)

            # 1.2 Dict, Class, Dataclass...
            else:
                decoded = self._decode_dict(value)

        # 3. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if Mapping Types:
            - `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`
        """

        # 1. ...
        return self._is_dict(value) or is_dataclass(value) or isinstance(value, Enum)

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if Mapping Types:
            - `class` (user defined classes), `dataclasses.dataclass`, `dict`, `Enum`
        """

        # 1. ...
        is_decode = False

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Checks...
            if _type in (
                SupportedTypes.CLASS.value,
                SupportedTypes.DATACLASS.value,
                SupportedTypes.DICT.value,
                SupportedTypes.ENUM.value
            ):

                # 2.1 ...
                is_decode = True

        # 3. ...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _is_dict(self, value):
        """ Checks if Dict Like Value """

        # 1. ...
        return isinstance(value, dict) or hasattr(value, EConst.DICT)

    # ----------------------------------------------------------------------------------------- #

    def _encode_enum(self, value: Enum):
        """ Encodes the Enum """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, Enum):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.ENUM.value,
                EConst.CLASS: ut.get_class_name(value),
                EConst.DATA: self._encode_as_dict(value.value)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: Enum. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_enum(self, value: dict):
        """ Decodes to Enum """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Reconstructs...
            cls_enum = ut.get_class(value)
            if cls_enum is not None:

                # 2.1 Decodes...
                val = self._decode_from_dict(value[EConst.DATA])
                output = cls_enum(val)

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid enum input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_dict(self, value):
        """ Encodes the value """

        # 1. ...
        encoded = None
        if self._is_dict(value):

            # 1.1 ...
            serialized_dict = {}
            for key, val in vars(value).items() if hasattr(value, EConst.DICT) else value.items():

                # 2.1 Validates...
                if not (isinstance(key, str) and key.startswith("___")):
                    mangled_name = ut.get_mangled_name(value)

                    # 3.1 Private and Protected...
                    process = True
                    if isinstance(key, str):

                        # 4.1 Private key (starts with double underscore)...
                        if key.startswith("__") or key.startswith(mangled_name):
                            if not self.enc_private:
                                process = False

                        # 4.2 Protected key (starts with double underscore)...
                        elif key.startswith("_") and not self.enc_protected:
                            process = False

                        # 4.3 Private or Procted...
                        if not process:
                            enc_key = self._encode_as_str(key)
                            serialized_dict[enc_key] = None

                    # 3.2 Valid keys...
                    if process:

                        # 4.1 Encodes Key...
                        enc_key = self._encode_as_str(key)
                        serialized_dict[enc_key] = self._encode_as_dict(val)

            # 1.2 ...
            encoded = {
                EConst.TYPE: self._get_defulat_type(value),
                EConst.CLASS: ut.get_class_name(value),
                EConst.DICT: serialized_dict,
            }

        # 2. ...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def _decode_dict(self, value):
        """ Decodes the value """

        # 1. ...
        decoded = {}
        if isinstance(value, dict) and (EConst.TYPE in value):

            # 1.1 Dict Items...
            dict_items = value[EConst.DICT].items() if (EConst.DICT in value) else value.items()
            if dict_items:

                # 2.1 Iterates to process...
                for key, val in dict_items:

                    # 3.1 ...
                    dec_key = self._decode_from_str(key)
                    decoded[dec_key] = self._decode_from_dict(val)

            # 1.2 If decoded and class was provided...
            cls = ut.get_class(value)
            if decoded and cls:

                # 2.1 Instance and Update...
                obj = cls.__new__(cls)
                if hasattr(obj, EConst.DICT):

                    # 3.1 Sets...
                    obj.__dict__.update(decoded)
                    decoded = obj

        # 2. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def _get_defulat_type(self, obj):

        # 1. ...
        tp = None
        if obj is not None:

            # 1.1 ...
            if isinstance(obj, dict):
                tp = SupportedTypes.DICT.value

            # 1.2 ...
            elif is_dataclass(obj):
                tp = SupportedTypes.DATACLASS.value

            # 1.3 ...
            else:
                tp = SupportedTypes.CLASS.value

        # 2. ...
        return tp

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
