import decimal

import numpy as np



normal_context = decimal.ROUND_HALF_UP
def set_vals():

    # context should set digits of precision,
    # Should use fractions for division
    pass
FLOAT_DTYPES = {
    np.dtypes.Float16DType,
    np.dtypes.Float32DType,
    np.dtypes.Float64DType,
}

FLOAT_DTYPE_INFO = {dtype: np.finfo(dtype) for dtype in FLOAT_DTYPES}
FLOAT_PRECISION_INFO_MAP = {
    np.dtypes.Float16DType: 16,
    np.dtypes.Float32DType: 32,
    np.dtypes.Float64DType: 64
}