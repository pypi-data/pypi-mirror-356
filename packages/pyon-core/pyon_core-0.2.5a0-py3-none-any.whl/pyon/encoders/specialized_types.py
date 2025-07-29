# --------------------------------------------------------------------------------------------- #
""" Pyon: Specialized Encoder """
# --------------------------------------------------------------------------------------------- #

import logging

# --------------------------------------------------------------------------------------------- #

from uuid import UUID

# --------------------------------------------------------------------------------------------- #

import numpy
import pandas

# --------------------------------------------------------------------------------------------- #

from bitarray import bitarray
from pandas.tseries.frequencies import to_offset

# --------------------------------------------------------------------------------------------- #

from ..file.api import File
from ..utils import EConst
from ..supported_types import SupportedTypes

# --------------------------------------------------------------------------------------------- #

from .. import utils as ut

# --------------------------------------------------------------------------------------------- #

from .base_encoder import BaseEncoder

# --------------------------------------------------------------------------------------------- #

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------------------------- #


class SpecEnc(BaseEncoder):
    """ Specialized Encoder """

    # ----------------------------------------------------------------------------------------- #

    _DF_INDEXES = {
        "Index",
        "RangeIndex",
        "MultiIndex",
        "DatetimeIndex",
        "TimedeltaIndex",
        "PeriodIndex",
        "CategoricalIndex",
        "Float64Index",
        "Int64Index",
        "UInt64Index"
    }

    # ----------------------------------------------------------------------------------------- #

    def encode(self, value):
        """ Encodes the Entity object """

        # 1. ...
        encoded = None
        if self.is_encode(value):

            # 1.1 Bitarray...
            if isinstance(value, bitarray):
                encoded = self._encode_bitarray(value)

            # 1.2 File...
            elif isinstance(value, File):
                encoded = self._encode_file(value)

            # 1.3 Numpy...
            elif isinstance(value, numpy.ndarray):
                encoded = self._encode_ndarray(value)

            # 1.4 UUID...
            elif isinstance(value, UUID):
                encoded = self._encode_uuid(value)

            # 1.5 DataFrames...
            elif isinstance(value, pandas.DataFrame):
                encoded = self._encode_dataframe(value)

            # 1.6 Series...
            elif isinstance(value, pandas.Series):
                encoded = self._encode_series(value)

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

            # 1.1 Bitarray...
            if _type == SupportedTypes.BITARRAY.value:
                decoded = self._decode_bitarray(value)

            # 1.2 File...
            elif _type == SupportedTypes.FILE.value:
                decoded = self._decode_file(value)

            # 1.3 Numpy...
            elif _type == SupportedTypes.NDARRAY.value:
                decoded = self._decode_ndarray(value)

            # 1.4 UUID...
            elif _type == SupportedTypes.UUID.value:
                decoded = self._decode_uuid(value)

            # 1.5 Dataframe...
            elif _type == SupportedTypes.DATAFRAME.value:
                decoded = self._decode_dataframe(value)

            # 1.6 Series...
            elif _type == SupportedTypes.SERIES.value:
                decoded = self._decode_series(value)

        # 3. ...
        return decoded

    # ----------------------------------------------------------------------------------------- #

    def is_encode(self, value):
        """ 
            Checks if encode of Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`
            - `pandas.DataFrame`, `pandas.Series`
        """

        # 1. ...
        return isinstance(
            value,
            (
                bitarray,
                numpy.ndarray,
                File,
                UUID,
                pandas.DataFrame,
                pandas.Series
            )
        )

    # ----------------------------------------------------------------------------------------- #

    def is_decode(self, value):
        """ 
            Checks if decode of Specialized Types:
            - `bitarray.bitarray`, `numpy.ndarray`, `pyon.File`, `uuid.UUID`
            - `pandas.DataFrame`, `pandas.Series`
        """

        # 1. ...
        is_decode = False

        # 2. ...
        if ut.is_decode_able(value):
            _type = value.get(EConst.TYPE)

            # 1.1 Checks...
            if _type in (
                SupportedTypes.BITARRAY.value,
                SupportedTypes.FILE.value,
                SupportedTypes.NDARRAY.value,
                SupportedTypes.UUID.value,
                SupportedTypes.DATAFRAME.value,
                SupportedTypes.SERIES.value
            ):

                # 2.1 ...
                is_decode = True

        # 3. ...
        return is_decode

    # ----------------------------------------------------------------------------------------- #

    def _encode_bitarray(self, value: bitarray):
        """ Encodes a bitarray object to a dictionary representation. """

        # 1. Checks input...
        encoded = None
        if (value is not None) and isinstance(value, bitarray):

            # 1.1 Encodes...
            encoded = {
                EConst.TYPE: SupportedTypes.BITARRAY.value,
                EConst.DATA: value.to01()
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: bitarray. Received: %s", type(value))

        # 3. Returns...
        return encoded

    # ----------------------------------------------------------------------------------------- #

    def _decode_bitarray(self, value: dict):
        """ Decodes a dictionary representation back to a bitarray object. """

        # 1. ...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 ...
            output = bitarray(value[EConst.DATA])

        # 2. ...
        else:

            # 1.1 ...
            logger.error(
                "Invalid bitarray input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. ...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_file(self, value: File):
        """ Encodes the file """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, File):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.FILE.value,
                EConst.DATA: value.to_dict(encode=True)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: File. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_file(self, value: dict):
        """ Decodes to File """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = File.from_dict(value[EConst.DATA])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid file input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_ndarray(self, value: numpy.ndarray):
        """ Encodes the Numpy ndarray """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, numpy.ndarray):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.NDARRAY.value,
                EConst.AUX1: value.shape,
                EConst.DATA: value.tolist(),
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: numpy.ndarray. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_ndarray(self, value: dict):
        """ Decodes to Numpy ndarray """

        # 1. Checks input...
        output = None
        if (
            (value is not None)
            and isinstance(value, dict)
            and (EConst.DATA in value)
            and (EConst.AUX1 in value)
        ):

            # 1.1 Decodes...
            np_array = numpy.array(value[EConst.DATA])
            output = np_array.reshape(value[EConst.AUX1])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid ndarray input. Expected: dict with %s and %s. Received: %s",
                EConst.DATA,
                EConst.AUX1,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_uuid(self, value: UUID):
        """ Encodes a UUID object to a string representation. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, UUID):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.UUID.value,
                EConst.DATA: str(value)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: UUID. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_uuid(self, value: dict):
        """ Decodes a string representation back to a UUID object. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Decodes...
            output = UUID(value[EConst.DATA])

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid UUID input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_dataframe(self, value: pandas.DataFrame):
        """ Encodes the DataFrame. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, pandas.DataFrame):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.DATAFRAME.value,
                EConst.DATA: self._encode_as_dict(value.to_dict(orient="records")),
                EConst.AUX1: self.__pre_encode(value.columns),
                EConst.AUX2: self.__pre_encode(value.index),
                EConst.AUX3: list(value.index.names),
                EConst.AUX4: type(value.index).__name__,
                EConst.AUX5: list(value.columns.names),
                EConst.AUX6: type(value.columns).__name__,
                EConst.AUX7: self.__index_freq(value.index)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: pandas.DataFrame. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_dataframe(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        output = None
        if isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Extracts components...
            data = self._decode_from_dict(value[EConst.DATA])

            # 1.2 Decodes: columns and index...
            columns = self.__decode_columns(value)
            index = self.__decode_index(value)

            # 1.3 Output...
            output = pandas.DataFrame(
                data=data, columns=columns, index=index
            )

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value),
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _encode_series(self, value: pandas.Series):
        """ Encodes the Series. """

        # 1. Checks input...
        output = None
        if (value is not None) and isinstance(value, pandas.Series):

            # 1.1 Encodes...
            output = {
                EConst.TYPE: SupportedTypes.SERIES.value,
                EConst.DATA: self._encode_as_dict(value.tolist()),
                EConst.AUX1: self.__pre_encode(value.index),
                EConst.AUX2: list(value.index.names),
                EConst.AUX3: type(value.index).__name__,
                EConst.AUX4: value.name,
                EConst.AUX5: self.__index_freq(value.index)
            }

        # 2. Logs if invalid...
        else:
            logger.error("Invalid input. Expected: pandas.Series. Received: %s", type(value))

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def _decode_series(self, value: dict):
        """ Decodes to a Series. """

        # 1. Checks input...
        output = None
        if isinstance(value, dict) and (EConst.DATA in value):

            # 1.1 Extracts components...
            series_data = self._decode_from_dict(value[EConst.DATA])
            index_data = value.get(EConst.AUX1)
            index_names = value.get(EConst.AUX2)
            index_type = value.get(EConst.AUX3)
            series_name = value.get(EConst.AUX4)
            series_freq = value.get(EConst.AUX5)

            # 1.2 Pre-decodes and rebuilds index...
            index_data = self.__pre_decode(index_data, index_type)
            index = self.__rebuild_index(index_data, index_names, index_type, series_freq)

            # 1.3 Builds Series...
            output = pandas.Series(data=series_data, index=index, name=series_name)

        # 2. If invalid...
        else:
            logger.error(
                "Invalid series input. Expected: dict with %s. Received: %s",
                EConst.DATA,
                type(value)
            )

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __decode_columns(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        columns = None
        if (
            isinstance(value, dict)
            and (EConst.AUX1 in value)
            and (EConst.AUX5 in value)
            and (EConst.AUX6 in value)
        ):

            # 1.1 Rebuilds columns...
            columns_data = value[EConst.AUX1]
            columns_names = value[EConst.AUX5]

            # 1.2 Pre decodes...
            columns_type = value[EConst.AUX6]
            columns_elements = self.__pre_decode(columns_data, columns_type)

            # 1.3 Multi Index...
            if columns_type == "MultiIndex":
                columns = pandas.MultiIndex.from_tuples(
                    columns_elements,  # type: ignore
                    names=columns_names
                )

            # 1.4 Other types...
            else:
                columns = pandas.Index(
                    columns_elements,
                    name=columns_names[0]
                    if columns_names
                    else None
                )

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s, %s, %s. Received: %s",
                EConst.AUX1,
                EConst.AUX5,
                EConst.AUX6,
                type(value),
            )

        # 3. Returns...
        return columns

    # ----------------------------------------------------------------------------------------- #

    def __decode_index(self, value: dict):
        """ Decodes to a DataFrame. """

        # 1. Checks input...
        index = None
        if (
            isinstance(value, dict)
            and (EConst.AUX2 in value)
            and (EConst.AUX3 in value)
            and (EConst.AUX4 in value)
        ):

            # 1.1 Extracts the index data...
            index_data = value[EConst.AUX2]
            index_names = value.get(EConst.AUX3)
            index_type = value.get(EConst.AUX4)
            index_freq = value.get(EConst.AUX7)

            # 1.2 Pre-decodes and rebuilds...
            index_data = self.__pre_decode(index_data, index_type)
            index = self.__rebuild_index(index_data, index_names, index_type, index_freq)

        # 2. If invalid...
        else:

            # 1.1 Logs...
            logger.error(
                "Invalid dataframe input. Expected: dict with %s, %s, %s. Received: %s",
                EConst.AUX2,
                EConst.AUX3,
                EConst.AUX4,
                type(value),
            )

        # 3. Returns...
        return index

    # ----------------------------------------------------------------------------------------- #

    def __is_arithmetic_range(self, seq):
        """Validates whether a sequence represents a regular arithmetic range."""

        # 1. ...
        return (
            isinstance(seq, list)
            and len(seq) >= 2
            and all((seq[i + 1] - seq[i]) == (seq[1] - seq[0]) for i in range(len(seq) - 1))
        )

    # ----------------------------------------------------------------------------------------- #

    def __build_range_index(self, seq, name):
        """Builds a pandas RangeIndex from a valid arithmetic sequence."""

        # 1. ...
        step = seq[1] - seq[0]

        # 2. ...
        start = seq[0]
        stop = seq[-1] + step

        # 3. ...
        return pandas.RangeIndex(start=start, stop=stop, step=step, name=name)

    # ----------------------------------------------------------------------------------------- #

    def __rebuild_index(self, index_data, index_names, index_type, freq=None):
        """ Rebuilds a pandas Index or subclass based on its serialized components. """

        # 1. Checks input...
        output = None
        index_name = index_names[0] if index_names else None

        # 2. Validates the index type...
        if index_type in self._DF_INDEXES:
            freq = to_offset(freq) if freq else None

            # 1.1 MultiIndex...
            if index_type == "MultiIndex":
                output = pandas.MultiIndex.from_tuples(index_data, names=index_names)

            # 1.2 RangeIndex...
            elif (index_type == "RangeIndex") and self.__is_arithmetic_range(index_data):
                output = self.__build_range_index(index_data, index_name)

            # 1.3 DatetimeIndex...
            elif index_type == "DatetimeIndex":
                output = pandas.DatetimeIndex(
                    index_data,
                    name=index_name,
                    freq=freq  # type: ignore
                )

            # 1.4 PeriodIndex...
            elif index_type == "PeriodIndex":
                output = pandas.PeriodIndex(index_data, name=index_name, freq=freq)

            # 1.5 TimedeltaIndex...
            elif index_type == "TimedeltaIndex":
                output = pandas.TimedeltaIndex(index_data, name=index_name)  # type: ignore

            # 1.6 CategoricalIndex...
            elif index_type == "CategoricalIndex":
                output = pandas.CategoricalIndex(index_data, name=index_name)

            # 1.7 Generic fallback...
            else:
                output = pandas.Index(index_data, name=index_name)

        # 3. Invalid type...
        else:
            logger.error("Invalid index type: %s", index_type)

        # 4. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __pre_encode(self, index):
        """ Converts the index into a JSON-safe list structure for serialization. """

        # 1. Checks for MultiIndex...
        if isinstance(index, pandas.MultiIndex):

            # 1.1 Converts tuples to lists...
            output = [list(x) for x in index.to_list()]

        # 2. Handles pandas-specific temporal types...
        else:

            # 1.1 Converts each element as needed...
            output = [
                str(x)
                if isinstance(x, (pandas.Timestamp, pandas.Period, pandas.Timedelta))
                else x
                for x in index
            ]

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __pre_decode(self, index_data, index_type):
        """ Reconstructs index elements after decoding from JSON-safe format. """

        # 1. MultiIndex elements are tuples...
        if index_type == "MultiIndex":
            output = [tuple(x) for x in index_data]

        # 2. DatetimeIndex...
        elif index_type == "DatetimeIndex":
            output = [pandas.Timestamp(x) for x in index_data]

        # 3. PeriodIndex...
        elif index_type == "PeriodIndex":
            output = [pandas.Period(x) for x in index_data]

        # 4. TimedeltaIndex...
        elif index_type == "TimedeltaIndex":
            output = [pandas.Timedelta(x) for x in index_data]

        # 5. Fallback: keep as-is...
        else:
            output = index_data

        # 6. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #

    def __index_freq(self, index):
        """ Checks if the index has a frequency attribute. """

        # 1. Checks for Frequency...
        output = None
        if (
            isinstance(index, (pandas.DatetimeIndex, pandas.PeriodIndex))
            and index.freq is not None
        ):

            # 1.1 Outputs...
            output = index.freq.freqstr

        # 3. Returns...
        return output

    # ----------------------------------------------------------------------------------------- #


# --------------------------------------------------------------------------------------------- #
