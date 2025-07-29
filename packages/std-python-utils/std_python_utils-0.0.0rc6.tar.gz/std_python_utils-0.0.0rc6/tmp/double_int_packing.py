import decimal
import random
from _pydecimal import Decimal
from decimal import Decimal


test_prec = 1
dcontext = decimal.Context(prec=test_prec, rounding=decimal.ROUND_HALF_UP)

def get_floats():
    return [random.random() * 10 ** random.randint(0,test_prec) for _ in range(10)]

def get_decimals(floats):
    return [dcontext.create_decimal_from_float(i) for i in floats]

def get_ratio_tups(decimals):
    return [i.as_integer_ratio() for i in decimals]

def get_bit_lengths(tups):
    return [(i1.bit_length(), i2.bit_length()) for i1,i2 in tups]

floats = get_floats()
decimals = get_decimals(floats)
rtups = get_ratio_tups(decimals)
bit_lens = get_bit_lengths(rtups)
total_bit_lens = [sum(i) for i in bit_lens]

print('Floats:\n', floats)
print('Decimals:\n', decimals)
print('Ratio tuples:\n', rtups)
print('Bit lengths:\n', bit_lens)
print('Total bit lengths:\n', total_bit_lens)
print(decimal.getcontext())