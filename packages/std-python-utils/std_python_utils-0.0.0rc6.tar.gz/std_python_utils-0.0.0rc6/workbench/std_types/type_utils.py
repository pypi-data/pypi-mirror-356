from numbers import Number
from typing import Optional, Set

import numpy as np

from workbench.std_types.float import FLOAT_DTYPES
from workbench.std_types.int import INT_DTYPES, UINT_DTYPES
from workbench.std_types.numeric import NUMERIC_DTYPE_INFO, NUMERIC_DTYPES, NUMERIC_PRECISION_INFO_MAP


def get_min_type_suggestion(
    type_set: Set[NUMERIC_DTYPES],
    min: Number,
    max: Number,
    min_precision: int,
    default: Optional[NUMERIC_DTYPES] = None
) -> np.dtype:
    for dtype in type_set:
        dtype_info = NUMERIC_DTYPE_INFO[dtype]
        if min >= dtype_info.min and max <= dtype_info.max and NUMERIC_PRECISION_INFO_MAP[dtype] >= min_precision:
            return dtype
    if default:
        return default

    raise ValueError(f"No suitable type found for min={min} and max={max} in {type_set}")


def get_min_uint_type_suggestion(
    max: Number = 0
) -> np.dtype:
    return get_min_type_suggestion(UINT_DTYPES, 0, max, 8)


def get_min_int_type_suggestion(
    min: Number = 0,
    max: Number = 0,
    min_precision: Optional[int] = 8
) -> np.dtype:
    if min < 0:
        return get_min_type_suggestion(INT_DTYPES, min, max, min_precision)

    return get_min_uint_type_suggestion(max)

def get_min_float_type_suggestion(
    min: Number = 0,
    max: Number = 0,
    min_precision: Optional[int] = 16
) -> np.dtype:

    return get_min_type_suggestion(FLOAT_DTYPES, min, max, min_precision)


def get_min_numeric_type_suggestion(
    min: Number = 0,
    max: Number = 0,
    int_only: bool = False,
    min_precision: Optional[int] = None
) -> np.dtype:
    if int_only:
        return get_min_int_type_suggestion(min, max, min_precision)

    return get_min_float_type_suggestion(min, max, min_precision)

