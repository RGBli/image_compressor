import math


def cal_bytes(size, unit):
    factor = 1000
    if unit == 'mb':
        factor = factor * 1000
    return size * factor
