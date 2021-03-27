import numpy as np
from .commons import quantiles as Q


def crps(f, y):
    """
    calculate crps metric
    :param f: predicted quantiles (.1, .25, .5, .75, .9)
    :param y: true value
    :return: crps metric
    """
    result = 0.
    i = 0
    for x_start, x_end in zip(Q[:-1], Q[1:]):
        f_mean = (f[i] + f[i + 1]) / 2
        i += 1
        if x_end < y:
            result += (x_end - x_start) * (f_mean**2)
        elif x_start <= y < x_end:
            result += (y - x_start) * (f_mean**2)
            result += (x_end - y) * ((f_mean - 1.)**2)
        else:
            result += (x_end - x_start) * ((f_mean - 1)**2)
    return result
