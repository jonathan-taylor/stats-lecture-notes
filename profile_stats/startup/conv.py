import numpy as np

def conv_binom(p, n):
    """
    Compute the pmf of the Binomial(n,p)
    by direct convolution.
    """
    d = [1-p,p]
    pq = [1-p,p]
    for _ in range(n-1):
        d = np.convolve(d, pq)
    d = np.array(d)
    return np.arange(d.shape[0]), d

def conv_integer_rv(d, n):
    """
    Compute the pmf of the convolution of
    non-negative integer valued random variable 
    by direct convolution.
    """
    dc = d.copy()
    for _ in range(n-1):
        d = np.convolve(d, dc)
    d = np.array(d)
    return np.arange(d.shape[0]), d

