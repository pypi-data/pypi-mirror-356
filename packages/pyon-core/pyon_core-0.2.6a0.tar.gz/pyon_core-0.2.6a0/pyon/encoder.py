""" Pyon: Python Object Notation - Encoder """
# --------------------------------------------------------------------------------------------- #

import json
import logging

# --------------------------------------------------------------------------------------------- #

from .encoders import BaseEnc, ColEnc, DateEnc, SpecEnc, NumEnc, MapEnc

# --------------------------------------------------------------------------------------------- #

from . import utils as ut

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class PyonEncoder():
    """ Pyon Encoder """

    # ----------------------------------------------------------------------------------------- #

    def __init__(self, enc_protected: bool = False, enc_private: bool = False):
        """ Initializes a Pyon Encoder """

        # 1. ...
        self.base_enc = BaseEnc()
        self.date_enc = DateEnc()
        self.num_enc = NumEnc()

        # 2. ...
        self.spec_enc = SpecEnc(self)
        self.col_enc = ColEnc(self)

        # 3. ...
        self.map_enc = MapEnc(self, enc_protected=enc_protected, enc_private=enc_private)

    # ----------------------------------------------------------------------------------------- #

    def encode_dict(self, value):
        """ Encodes the Entity object """

        # 1. ...
        encoded = None
        if value is not None:

            # 1.1 Base Types...
            if self.base_enc.is_encode(value):
                encoded = self.base_enc.encode(value)

            # 1.2 Numeric Types...
            elif self.num_enc.is_encode(value):
                encoded = self.num_enc.encode(value)

            # 1.3 Collection Types...
            elif self.col_enc.is_encode(value):
                encoded = self.col_enc.encode(value)

            # 1.4 Datetime Types...
            elif self.date_enc.is_encode(value):
                encoded = self.date_enc.encode(value)

            # 1.5 Specialized Types...
            elif self.spec_enc.is_encode(value):
                encoded = self.spec_enc.encode(value)

            # 1.6 Mapping Types...
            elif self.map_enc.is_encode(value):
                encoded = self.map_enc.encode(value)

        # 2. ...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def decode_dict(self, value):
        """ Decodes the value """

        # 1. ...
        decoded = None
        if ut.is_decode_able(value):

            # 1.1 Numeric Types...
            if self.num_enc.is_decode(value):
                decoded = self.num_enc.decode(value)

            # 1.2 Collection Types...
            elif self.col_enc.is_decode(value):
                decoded = self.col_enc.decode(value)

            # 1.3 Datetime Types...
            elif self.date_enc.is_decode(value):
                decoded = self.date_enc.decode(value)

            # 1.4 Specialized Types...
            elif self.spec_enc.is_decode(value):
                decoded = self.spec_enc.decode(value)

            # 1.5 Mapping Types...
            elif self.map_enc.is_decode(value):
                decoded = self.map_enc.decode(value)

        # 2. Base Types...
        elif self.base_enc.is_decode(value):
            decoded = self.base_enc.decode(value)

        # 3. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def encode_str(self, obj):
        """ Exports to pyon. """

        # 1. ...
        output = None
        if obj is not None:

            # 1.1 ...
            encoded = self.encode_dict(obj)

            # 1.2 ...
            if encoded is not None:
                output = json.dumps(encoded, ensure_ascii=False, indent=3)

            # 1.3 ...
            else:
                logger.error("Object '%s' failed to be encoded.", type(obj).__name__)

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def decode_str(self, pyon_str: str):
        """ Imports from pyon string. """

        # 1. ...
        output = None
        if pyon_str is not None:

            # 1.1 ...
            dictionary = json.loads(pyon_str)
            if dictionary is not None:

                # 2.1 ...
                output = self.decode_dict(dictionary)

            # 1.2 ...
            else:
                logger.error("Input failed to be decoded.")

        # 2. ...
        return output

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
