import numpy as np
from numba import jit


@jit
def qwk3(a1, a2, max_rat):
    """
    Calculates the quadratic weighted kappa between two classifications, `a1` and `a2`.

    :param a1: A list of integers corresponding to the labels assigned by the first annotator.
    :param a2: A list of integers corresponding to the labels assigned by the second annotator.
    :param max_rat: The number of categories (I think)
    :return:
    """
    assert len(a1) == len(a2)
    a1 = np.asarray(a1, dtype=int)
    a2 = np.asarray(a2, dtype=int)

    hist1 = np.zeros((max_rat + 1,))
    hist2 = np.zeros((max_rat + 1,))

    o = 0
    for k in range(a1.shape[0]):
        i, j = a1[k], a2[k]
        hist1[i] += 1
        hist2[j] += 1
        o += (i - j) * (i - j)

    e = 0
    for i in range(max_rat + 1):
        for j in range(max_rat + 1):
            e += hist1[i] * hist2[j] * (i - j) * (i - j)

    e = e / a1.shape[0]

    return 1 - o / e
