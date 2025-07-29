from collections import ChainMap

import numpy as np


QUARTER_INT_DTYPES = frozenset({
    np.dtypes.UInt8DType,
    np.dtypes.Int8DType
})

HALF_INT_DTYPES = frozenset({
    np.dtypes.Int16DType,
    np.dtypes.UInt16DType
})

SINGLE_INT_DTYPES = frozenset({
    np.dtypes.Int32DType,
    np.dtypes.UInt32DType
})

DOUBLE_INT_DTYPES = frozenset({
    np.dtypes.Int64DType,
    np.dtypes.UInt64DType
})

UINT_DTYPES = frozenset({
    np.dtypes.UInt8DType,
    np.dtypes.UInt16DType,
    np.dtypes.UInt32DType,
    np.dtypes.UInt64DType
})

BigInt = int
SINT_DTYPES = {
    np.dtypes.Int8DType,
    np.dtypes.Int16DType,
    np.dtypes.Int32DType,
    np.dtypes.Int64DType,
    BigInt
}

INT_DTYPES = SINT_DTYPES | UINT_DTYPES

UINT_DTYPE_INFO = {dtype: np.iinfo(dtype) for dtype in UINT_DTYPES}
SINT_DTYPE_INFO = {dtype: np.iinfo(dtype) for dtype in SINT_DTYPES}
INT_DTYPE_INFO = ChainMap(SINT_DTYPE_INFO, UINT_DTYPE_INFO)

INT_PRECISION_INFO_MAP = {
    **{dtype: 8 for dtype in QUARTER_INT_DTYPES},
    **{dtype: 16 for dtype in HALF_INT_DTYPES},
    **{dtype: 32 for dtype in SINGLE_INT_DTYPES},
    **{dtype: 64 for dtype in DOUBLE_INT_DTYPES}
}

