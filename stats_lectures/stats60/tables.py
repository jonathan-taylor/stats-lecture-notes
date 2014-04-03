import numpy as np
from scipy.stats import norm as ndist
from ipy_table import make_table

def table_a104(z):
    """
    Produce a row of Table A104
    """
    if z < 0:
        raise ValueError('z must be nonnegative')
    table = [('$z$', 'Height', 'Area'),
             (z, 100*ndist.pdf(z), 100*2*(ndist.cdf(z)-0.5))]
    return make_table(table)

