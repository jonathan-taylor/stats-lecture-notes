import itertools
from pkg_resources import resource_stream

import matplotlib.pyplot as plt
import numpy as np
from base64 import encodestring
import PIL.Image
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML

from examples import BoxModel, ProbabilitySpace, RandomVariable

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
                if (i, j, color, alpha) not in _dice_cache:
                    _dice_cache[(i,j,color,alpha)] = dice_html((i,j),
                                                              color_alpha=(color, 0.5))
                dice_row += '<td>' + _dice_cache[(i,j,color,alpha)] + '</td>'
            else:
                if (i, j) not in _dice_cache:
                    _dice_cache[(i,j)] = dice_html((i,j))
                dice_row += '<td>' + _dice_cache[(i,j)] + '</td>'
        dice_row += '</tr>'
        dice_str += dice_row + '\n'
    return dice_str + '</table>\n'

def sum_to_seven_test(outcome):
    i, j = outcome
    return i + j == 7

def sum_geq_eight_test(outcome):
    i, j = outcome
    return i + j >= 8

def dice_trial(event = sum_to_seven_test,
               outcome=None, color="#0000aa", alpha=0.5,
               success='#00aa00',
               failure='#aa0000'):
    """
    dice_table with all outcomes who evaluate to true by `event`
    colored `color`

    Parameters
    ----------

    outcome : (int, int) [optional]
        Outcome of rolling the dice.
    
    color : color 
        Color to label those that pass random_variable
    """
    colors = {}
    for i, j in itertools.product(range(1,7), range(1,7)):
        if event((i,j)):
            colors[(i,j)] = color

    if outcome is not None:
        iout, jout = outcome
        if (iout, jout) in colors:
            colors[(iout,jout)] = success
        else:
            colors[(iout,jout)] = failure

    return dice_table(colors, alpha=alpha)

class dice_example(ProbabilitySpace):

    desc = 'An example consisting of rolling two dice.'

    def __init__(self, event_spec=None,
                 random_variable=None,
                 color="#0000aa", alpha=0.5,
                 success='#00aa00',
                 failure='#aa0000'):

        if event_spec is not None and random_variable is not None:
            raise ValueError('can only specify `event_spec` or `random_variable`')

        sample_space = [(i,j) for i, j in itertools.product(range(1,7), range(1,7))]

        if event_spec is not None:
            self.model = BoxModel(sample_space).event(event_spec)
            self.model_type = 'event'
        elif random_variable is None:
            self.model = BoxModel(sample_space)
            self.model_type = 'pair of dice'
        else:
            self.model = RandomVariable(BoxModel(sample_space), random_variable)
            self.model_type = 'random variable'

        # all related to _repr_html_ output
        self.success = success
        self.failure = failure
        self.color = color
        self.alpha = alpha

        self.outcome = None

    @property
    def mass_function(self):
        return self.model.mass_function

    @property
    def sample_space(self):
        return self.model.sample_space

    def trial(self):
        self.outcome = self.model.trial()
        return self.outcome
                        
    def _repr_html_(self):
        if self.model_type == 'event':
            base = dice_trial(event=self.model.random_variable,
                              outcome=self.model.probability_space.outcome,
                              color=self.color,
                              failure=self.failure,
                              success=self.success,
                              alpha=self.alpha)
        elif self.model_type == 'pair of dice':
            base = dice_trial(event=lambda outcome: False,
                              outcome=self.model.outcome,
                              color=None,
                              failure=self.failure,
                              success=self.success,
                              alpha=self.alpha)
        elif self.model_type == 'random variable':
            base = dice_trial(event=lambda outcome: False,
                              outcome=self.model.probability_space.outcome,
                              color=None,
                              failure=self.failure,
                              success=self.success,
                              alpha=self.alpha)
            base += '<h3>Outcome is: %s</h3>' % `self.outcome`
        return base

sum_to_seven = dice_example(event_spec=[(1,6),(2,5),(3,4),(4,3),(5,2),(6,1)])
sum_geq_eight = dice_example(event_spec= lambda outcome: outcome[0] + outcome[1] >= 8)
sum_of_values = dice_example(random_variable = lambda outcome: outcome[0] + outcome[1])
pair_of_dice = dice_example()

examples = {'sum to seven':sum_to_seven,
            'sum greater than seven':sum_geq_eight,
            'sum_of_values':sum_of_values,
            'pair of dice':pair_of_dice}

