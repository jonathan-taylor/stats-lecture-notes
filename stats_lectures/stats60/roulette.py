from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from base64 import encodestring
import PIL.Image
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML, display, Latex

from .probability import (BoxModel, ProbabilitySpace, 
                          Geometric, Binomial, RandomVariable)

_colors = {}
red_numbers = [1,3,5,7,9,12,14,16,18,19,21,23,25,27,30,32,34,36]
black_numbers = [2,4,6,8,10,11,13,15,17,20,22,24,26,28,29,31,33,35]

for i in red_numbers:
    _colors[i] = 'red'
for i in black_numbers:
    _colors[i] = 'black'

_colors['0'] = 'green'
_colors['00'] = 'green'

_places_cache = {}
def _html_place(s, radius=1, fontsize=120,
                facecolor='red', ax=None,
                correct=None,
                bg_alpha=None
                ):
    fig = plt.figure(figsize=(4,4))
    ax = fig.gca()
    ax.set_xlim([-1.2,1.2])
    ax.set_ylim([-1.2,1.2])

    if correct is not None:
        alpha=0.25
        if correct:
            ax.scatter([0,0], [0,0], s=55000, marker=r'$\checkmark$', color='green')

        else:
            ax.scatter([0,0], [0,0], s=55000, marker=r'x', color='red',
                       linewidth=15)
    else:
        alpha = 1.

    circle = Circle((0,0), 1., facecolor=facecolor,
                    edgecolor='k', alpha=alpha)
    ax.add_patch(circle)
    ax.text(0, 0, s,
            horizontalalignment='center',
            verticalalignment='center', 
            fontsize=fontsize,
            color='white', alpha=alpha)
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])

    if bg_alpha is not None:
        bg, alpha = bg_alpha
        rec = Rectangle((-2,-2), 4, 4, facecolor=bg, 
                        alpha=alpha, fill=True)
        ax.add_patch(rec)

    plt.draw()
    ax.set_xlim([-1.2,1.2])
    ax.set_ylim([-1.2,1.2])

    place_png = print_figure(fig, 'png')
    plt.close()
    place_png64 = encodestring(place_png).decode('ascii')
    return '<img src="data:image/png;base64,%s" height="150" width="150">' % place_png64

class roulette_position(object):

    desc = 'An example of spinning a roulette wheel.'

    def __init__(self, place, facecolor="red",
                 bg_alpha=None,
                 correct=None,
                 fontsize=120):
        self.place = place
        self.facecolor = facecolor
        self.bg_alpha = bg_alpha
        self.correct = correct
        self.fontsize = fontsize

    def _repr_html_(self):
        key = (self.place, self.facecolor, self.bg_alpha, self.correct)
        if (key not in _places_cache):
            _places_cache[key] = _html_place(self.place,
                                             facecolor=self.facecolor,
                                             bg_alpha=self.bg_alpha,
                                             correct=self.correct,
                                             fontsize=self.fontsize)
        return _places_cache[key]

empty_table = {}
for place in range(1,37):
    empty_table[place] = roulette_position(place,
                                        facecolor=_colors[place])
empty_table['0'] = roulette_position('0', facecolor=_colors['0'])
empty_table['00'] = roulette_position('00', facecolor=_colors['00'])


def roulette_table(places=empty_table):

    """
    Return a table of all 36 possible
    values for a pair of roulette.

    Parameters
    ----------

    places : {}
        Dict of `roulette_position` instances.

    Returns
    -------

    table_html : str
        HTML version of all outcomes roulette as a <table>.

    """

    roulette_str = '<table>'
    rows = [range(1,37,3) + ['0'],
            range(2,38,3) + ['00'],
            range(3,39,3)]

    for row in rows:
        roulette_row = '<tr>'
        for place in row:
            roulette_row += '<td>' + places[place]._repr_html_() + '</td>'
        roulette_row += '</tr>'
        roulette_str += roulette_row + '\n'
    return roulette_str + '</table>\n'

def odd_test(outcome):
    return outcome in range(1, 36, 2)

def red_test(outcome):
    return outcome in red_numbers

def black_test(outcome):
    return outcome in black_numbers

def roulette_trial(event_spec = odd_test,
                   outcome=None, betcolor="#0000aa", alpha=0.25):
    """
    roulette_table with all outcomes who evaluate to true by `event_spec`
    colored `color`

    Parameters
    ----------

    outcome : (int, int) [optional]
        Outcome of rolling the roulette.
    
    betcolor : color 
        Color to label those that pass event_spec
    """
    places = {}
    pass_test = []
    for place in range(1,37):
        if event_spec(place):
            pass_test.append(place)
            places[place] = roulette_position(place,
                                           facecolor=_colors[place],
                                           bg_alpha=(betcolor, alpha))
        else:
            places[place] = roulette_position(place,
                                           facecolor=_colors[place])

    if outcome is not None:
        if outcome in pass_test:
            places[outcome] = roulette_position(outcome,
                                                facecolor=_colors[place],
                                                bg_alpha=(betcolor, alpha),
                                                correct=True)
        else:
            places[outcome] = roulette_position(outcome,
                                                facecolor=_colors[place],
                                                correct=False)

    places['0'] = roulette_position('0', facecolor=_colors['0'])
    places['00'] = roulette_position('00', facecolor=_colors['00'])

    return roulette_table(places)

class roulette_example(ProbabilitySpace):

    def __init__(self, event_spec=None,
                 betcolor="#0000aa", alpha=0.25):
        self.betcolor = betcolor
        self.alpha = alpha

        sample_space = range(1,37) + ['0', '00']
        self.event_spec = event_spec
        self.position = None

        if event_spec is not None:
            self.model = BoxModel(sample_space).event(event_spec)
            self.model_type = 'event'
        elif event_spec is None:
            self.model = BoxModel(sample_space)
            self.model_type = 'spin of wheel'

    @property
    def mass_function(self):
        return self.model.mass_function

    @property
    def sample_space(self):
        return self.model.sample_space

    def trial(self):
        self.outcome = self.model.trial()
        if self.model_type == 'event':
            self.position = self.model.probability_space.outcome
        else:
            self.position = self.outcome
        return self.outcome

    def _repr_html_(self):
        return roulette_trial(event_spec=self.event_spec,
                              outcome=self.position,
                              betcolor=self.betcolor,
                              alpha=self.alpha)

odd_numbers = roulette_example(event_spec=odd_test)
odd_numbers.desc = 'A roulette bet on only odd numbers.'

red = roulette_example(event_spec=red_test)
red.desc = 'A roulette bet on red numbers.'

red_bet10 = RandomVariable(red, lambda outcome: 10 * (2 * outcome - 1))

def bet(event, amount, ntimes, initial_amount=0):
    odds = (len(range(1,37)) - len(event)) / len(event)
    binom = Binomial(ntimes, BoxModel(sample_space), event)
    rv = RandomVariable(binom, lambda outcome : amount * (odds * outcome - (ntimes - outcome)) + initial_amount)
    return rv

five = roulette_example(event_spec=lambda outcome: outcome == 5)
five.desc = 'A roulette bet on red numbers.'

sample_space = range(1,37) + ['0', '00']
sixplays_five = Binomial(6, BoxModel(sample_space), [5])
eightplays_red = Binomial(8, BoxModel(sample_space), red_numbers)

black = roulette_example(event_spec=black_test)
black.desc = 'A roulette bet on black  numbers.'

def middle_test(outcome):
    return outcome in range(13, 25)

middle_third = roulette_example(event_spec=range(13,25))
middle_third.desc = 'A roulette bet on only the middle third of the possible numbers.'

special_bet = roulette_example(event_spec=[2,24,29])
special_bet.desc = 'A roulette bet on [2,24,29].'

class roulette_geometric(roulette_example):

    def __init__(self, event_spec = odd_test,
                 betcolor="#0000aa", alpha=0.25):

        roulette_example.__init__(self, event_spec,
                                  betcolor, alpha)

        # overwrite the model
        self.model = Geometric(BoxModel(range(1,37)+['0','00']), event_spec)


odd_waiting = roulette_geometric(odd_test)
odd_waiting.desc = 'Waiting time until an odd number is rolled.'

special_bet_waiting = roulette_geometric([2,24,29])
special_bet.desc = 'Waiting time until one of [2,24,29] is rolled.'

examples = {'odd numbers':odd_numbers, 
            'special_bet':special_bet,
            'middle third':middle_third,
            'time until odd':odd_waiting,
            'time until special':special_bet_waiting,
            'red':red,
            'black':black}

