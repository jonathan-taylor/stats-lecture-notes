import itertools
from pkg_resources import resource_stream

import matplotlib.pyplot as plt
import numpy as np
from base64 import encodestring
import PIL.Image
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML

_dice_arrays = {}

def die(digit, size=(150,150)):
    """
    Load in die from GIF file, returning
    as an RGBA array, resized to `size`.

    Parameters
    ----------

    digit : int
        Which die (from 1 to 6)

    size : (int, int)
        What size to return 

    Returns
    -------

    img : np.array(size + (4,))
        RGBA version of die.

    """
    if digit not in _dice_arrays:
        img = PIL.Image.open(resource_stream('stats_lectures', 'data/die%d.gif' % digit))
        _dice_arrays[digit] = img.crop((156,133,440,416))
    return np.array(_dice_arrays[digit].resize(size).convert('RGBA'))

def dice(digits,size=(150,150)):
    """
    Return pair of dice, side by side.

    Parameters
    ----------

    digits : (int, int)
        Which dice (from 1 to 6)

    size : (int, int)
        What size each die will be. Return value will
        be 1.2 times as high and 2.4 times as wide.

    Returns
    -------

    img : np.array(size + (4,))
        RGBA version of dice.

    """

    output = np.zeros((size[0]*1.2,2.4*size[1],4), np.uint8)
    img1, img2 = [die(digits[i]) for i in range(2)]
    output[0.1*size[0]:1.1*size[0],0.1*size[1]:1.1*size[1]] = img1[:(1.1*size[0]-0.1*size[0]),:(1.1*size[1]-0.1*size[1])]
    output[0.1*size[0]:1.1*size[0]:,1.3*size[1]:2.3*size[1]] = img2[:(1.1*size[0]-0.1*size[0]),:(2.3*size[1]-1.3*size[1])]
    return output


def dice_html(digits, color_alpha=None):
    """
    Return pair of dice, side by side as HTML img.
    If color_alpha is not None, then the black and white
    pair of dice will be blended as if they were labelled
    with a particular color.

    Parameters
    ----------

    digits : (int, int)
        Which dice (from 1 to 6)

    color_alpha : (color_hex, float)
        The first argument should be a color as
        in hex string format, (i.e. "#820000")
        while the second is an alpha value between 0 and 1.

    Returns
    -------

    img_html : str
        HTML version of dice as an <img>.

    """

    dice_arr = dice(digits)
    color_arr = np.ones(dice_arr.shape, np.uint8)
    if color_alpha is not None:
        color, alpha = color_alpha
        color_arr[:,:,0] = eval('0x%s' % color[1:3])
        color_arr[:,:,1] = eval('0x%s' % color[3:5])
        color_arr[:,:,2] = eval('0x%s' % color[5:7])
        color_arr[:,:,3] = 255
        dice_arr[:] = (1 - alpha) * dice_arr + alpha * color_arr
        
    f = plt.figure()
    ax = f.gca()
    ax.imshow(dice_arr)
    ax.set_xticks([])
    ax.set_yticks([])
    ax.set_frame_on(False)
    dice_png = print_figure(f, 'png')
    plt.close()
    dice_png64 = encodestring(dice_png).decode('ascii')
    return '<img src="data:image/png;base64,%s" height="150" width="150">' % dice_png64

_dice_cache = {}
def dice_table(colors={}, alpha=0.5):

    """
    Return a table of all 36 possible
    values for a pair of dice.

    Parameters
    ----------

   colors : {}
        Dict indexed by digit pairs which
        determine what color to label this
        outcome.

    alpha : float
        Used in dice_html to blend all colors.

    Returns
    -------

    table_html : str
        HTML version of all outcomes dice as a <table>.

    """

    dice_str = '<table>'
    for i in range(1,7):
        dice_row = '<tr>'
        for j in range(1,7):
            color = colors.get((i,j), None)
            if color:
                if (j, i, color, alpha) not in _dice_cache:
                    _dice_cache[(j,i,color,alpha)] = dice_html((j,i),
                                                              color_alpha=(color, 0.5))
                dice_row += '<td>' + _dice_cache[(j,i,color,alpha)] + '</td>'
            else:
                if (j, i) not in _dice_cache:
                    _dice_cache[(j,i)] = dice_html((j,i))
                dice_row += '<td>' + _dice_cache[(j,i)] + '</td>'
        dice_row += '</tr>'
        dice_str += dice_row + '\n'
    return dice_str + '</table>\n'

def dice_trial(testfn = lambda i,j : (i+j)==7,
               outcome=None, color="#0000aa", alpha=0.5,
               success='#00aa00',
               failure='#aa0000'):
    """
    dice_table with all outcomes who evaluate to true by `testfn`
    colored `color`

    Parameters
    ----------

    outcome : (int, int) [optional]
        Outcome of rolling the dice.
    
    color : color 
        Color to label those that pass testfn
    """
    colors = {}
    for i, j in itertools.product(range(1,7), range(1,7)):
        if testfn(i,j):
            colors[(i,j)] = color

    if outcome is not None:
        iout, jout = outcome
        if (iout, jout) in colors:
            colors[(iout,jout)] = success
        else:
            colors[(iout,jout)] = failure

    return dice_table(colors, alpha=alpha)

class dice_example(object):

    def __init__(self, testfn = lambda i,j : (i+j)==7,
                 color="#0000aa", alpha=0.5,
                 success='#00aa00',
                 failure='#aa0000'):
        self.success = success
        self.failure = failure
        self.color = color
        self.alpha = alpha
        self.testfn = testfn

        self.ntrial = 0
        self.nsuccess = 0
        self.outcome = None

    def reset(self):
        self.outcome = None
        self.ntrial = 0

    def trial(self):
        """
        Run a trial, incrementint success counter and updating
        html output
        """
        self.outcome = tuple(np.random.random_integers(1,6,size=(2,)))
        self.nsuccess += self.testfn(*self.outcome)
        self.ntrial += 1
        return self

    def _repr_html_(self):
        base = dice_trial(testfn=self.testfn,
                          outcome=self.outcome,
                          color=self.color,
                          failure=self.failure,
                          success=self.success,
                          alpha=self.alpha)
        if self.ntrial > 0:
            base += '<h3>Success rate: %d out of %d: %d%%</h3>' % (self.nsuccess, self.ntrial, self.nsuccess*100./self.ntrial)
        return base

sum_to_seven = dice_example()
sum_geq_eight = dice_example(testfn = lambda i, j : i+j >= 8)
