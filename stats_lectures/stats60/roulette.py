from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from base64 import encodestring
import PIL.Image
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML, display, Latex

from .examples import bernoulli, geometric

_colors = {}
for i in range(1,37):
    if i % 2 == 0:
        _colors[i] = 'black'
    else:
        _colors[i] = 'red'
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
                 correct=None):
        self.place = place
        self.facecolor = facecolor
        self.bg_alpha = bg_alpha
        self.correct = correct
    
    def _repr_html_(self):
        key = (self.place, self.facecolor, self.bg_alpha, self.correct)
        if (key not in _places_cache):
            _places_cache[key] = _html_place(self.place,
                                             facecolor=self.facecolor,
                                             bg_alpha=self.bg_alpha,
                                             correct=self.correct)
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

def roulette_trial(testfn = odd_test,
                   outcome=None, betcolor="#0000aa", alpha=0.25):
    """
    roulette_table with all outcomes who evaluate to true by `testfn`
    colored `color`

    Parameters
    ----------

    outcome : (int, int) [optional]
        Outcome of rolling the roulette.
    
    betcolor : color 
        Color to label those that pass testfn
    """
    places = {}
    pass_test = []
    for place in range(1,37):
        if testfn(place):
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

class roulette_example(bernoulli):

    def __init__(self, testfn = odd_test,
                 betcolor="#0000aa", alpha=0.25):
        self.betcolor = betcolor
        self.alpha = alpha

        bernoulli.__init__(self, testfn)

    @property
    def sample_space(self):
        return range(1,37) + ['0', '00']

    @property
    def mass_function(self):
        ss = self.sample_space
        return dict([(v, 1./len(ss)) for v in ss])

    def trial(self, numeric=False):
        """
        Run a trial, incrementint success counter and updating
        html output
        """
        self.outcome = np.random.random_integers(1,38)
        if self.outcome == 37:
            self.outcome = '0'
        elif self.outcome == 38:
            self.outcome = '00'
                             
        if self.outcome not in ['0', '00']:
            self.numeric_outcome = self.testfn(self.outcome)
        else:
            self.numeric_outcome = 0
        self.total += self.numeric_outcome
        self.total2 += self.numeric_outcome**2
        self.ntrial += 1
        if not numeric:
            return self.outcome
        return self.numeric_outcome

    def _repr_html_(self):
        base = roulette_trial(testfn=self.testfn,
                              outcome=self.outcome,
                              betcolor=self.betcolor,
                              alpha=self.alpha)
        if self.ntrial > 0:
            base += self.html_summary
        return base

odd_numbers = roulette_example()
odd_numbers.desc = 'A roulette bet on only odd numbers.'

def middle_test(outcome):
    return outcome in range(13, 25)

middle_third = roulette_example(testfn = middle_test)
middle_third.desc = 'A roulette bet on only the middle third of the possible numbers.'

def special_bet_test(outcome):
    return outcome in [2,24,29]

special_bet = roulette_example(testfn = special_bet_test)
special_bet.desc = 'A roulette bet on [2,24,29].'

class roulette_geometric(geometric):

    def __init__(self, testfn = odd_test,
                 betcolor="#0000aa", alpha=0.25):

        bernoulli = roulette_example(testfn, 
                                     betcolor=betcolor,
                                     alpha=alpha)
        geometric.__init__(self, bernoulli)


odd_waiting = roulette_geometric()
odd_waiting.desc = 'Waiting time until an odd number is rolled.'

special_bet_waiting = roulette_geometric(testfn=special_bet.testfn)
special_bet.desc = 'Waiting time until one of [2,4,29] is rolled.'

examples = {'odd numbers':odd_numbers, 
            'special_bet':special_bet,
            'middle third':middle_third,
            'time until odd':odd_waiting,
            'time until special':special_bet_waiting}
