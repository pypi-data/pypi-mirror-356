import numpy as np


def try_pack_float(val: float) -> bytes:
    ratio_vals = val.as_integer_ratio()
    numerator_size = ratio_vals[0].bit_length()
    denominator_size = ratio_vals[1].bit_length()


[(j, k) for i in range(20) for j, k in i.as_integer_ratio() if abs(j) > 1 and abs(k) > 1]