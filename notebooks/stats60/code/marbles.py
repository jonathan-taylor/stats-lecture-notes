from copy import copy
import numpy as np
from matplotlib.patches import Circle, Rectangle
from base64 import encodestring
import matplotlib.pyplot as plt
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML, display, Latex

# this should be top level of collection of notebooks
# TODO -- is there a better way?
import sys
sys.path.append('..')
from probability import BoxModel

_marble_cache = {}

for symb, col in zip(['B', 'R'], ['blue', 'red']):

    fig = plt.figure(figsize=(4,4))
    ax = fig.gca()
    ax.set_xlim([-1.2,1.2])
    ax.set_ylim([-1.2,1.2])

    circle = Circle((0,0), 1., facecolor=col,
                    edgecolor='k', alpha=1.0)
    ax.add_patch(circle)
    ax.set_frame_on(False)
    ax.set_xticks([])
    ax.set_yticks([])

    plt.draw()
    ax.set_xlim([-1.2,1.2])
    ax.set_ylim([-1.2,1.2])

    marble_png = print_figure(fig, 'png')
    marble_png64 = encodestring(marble_png).decode('ascii')
    _marble_cache[symb] = '<img src="data:image/png;base64,%s" height="40" width="40">' % marble_png64

    circle.set_alpha(0.25)
    ax.scatter([0,0], [0,0], s=55000, marker=r'$\checkmark$', color='green')
    marble_png = print_figure(fig, 'png')
    marble_png64 = encodestring(marble_png).decode('ascii')
    _marble_cache[(symb,True)] = '<img src="data:image/png;base64,%s" height="40" width="40">' % marble_png64
    plt.close()

def numbered_marble(col, number):
    if (col, number) not in _marble_cache:
        fig = plt.figure(figsize=(4,4))
        ax = fig.gca()
        ax.set_xlim([-1.2,1.2])
        ax.set_ylim([-1.2,1.2])

        circle = Circle((0,0), 1., facecolor=col,
                        edgecolor='k', alpha=0.7)
        ax.add_patch(circle)
        ax.set_frame_on(False)
        ax.set_xticks([])
        ax.set_yticks([])
        ax.text(0, 0, str(number), fontsize=100,
                verticalalignment='center',
                horizontalalignment='center')
        plt.draw()
        ax.set_xlim([-1.2,1.2])
        ax.set_ylim([-1.2,1.2])

        marble_png = print_figure(fig, 'png')
        marble_png64 = encodestring(marble_png).decode('ascii')
        _marble_cache[(col, number)] = '<img src="data:image/png;base64,%s" height="40" width="40">' % marble_png64
        plt.close()
    return (col, number)

class Marbles(BoxModel):

    def __init__(self, values, grid=(-1,5), replace=True):
        values = copy(values)
        self.replace = replace
        self.grid = grid
        np.random.shuffle(values)
        BoxModel.__init__(self, values)
        self._cached_html_ = _html_box(self.values, grid=self.grid)
        self._drawn = []

    def trial(self):
        '''
        We update the box!
        '''
        try:
            outcome = np.random.random_integers(0, len(self.values)-1)
        except ValueError:
            return None
        self._cached_html_trial_ = _html_box(self.values, outcome=outcome, grid=self.grid)
        if not self.replace: # sampling without replacement
            V = self.values.pop(outcome)
            drawn = self._drawn + [V]
            Marbles.__init__(self, self.values,
                             grid=self.grid, replace=self.replace)
            self._drawn = drawn
            return V
        else:
            self._drawn.append(self.values[outcome])
            return self.values[outcome]

    def last_draw(self):
        if hasattr(self, "_cached_html_trial_"):
            return HTML(self._cached_html_trial_)

    def drawn_so_far(self):
        if self._drawn:
            return HTML(_html_box(self._drawn, grid=self.grid))

    def _repr_html_(self):
        return self._cached_html_

    def current_state(self):
        value = '<h2>Box</h2>' + self._repr_html_()
        if self._drawn:
            value += '<h2>Draws</h2>' + self.drawn_so_far().data
        return HTML(value)

def _html_box(values, outcome=None, grid=(2,3)):
    idx = 0
    stop = False
    _table = '<table>'
    while True:
        row = []
        for j in range(grid[1]):
            if idx < len(values):
                if outcome is not None and idx == outcome:
                    row.append(_marble_cache[(values[idx], True)])
                else:
                    row.append(_marble_cache[values[idx]])
            else:
                row.append('')
                stop = True
            idx += 1
        if ''.join(row):
            _table += '<tr>' + '\n'.join(['<td>%s</td>' % r for r in row if r]) + '</tr>'
        if stop:
            break

    return _table + '</table>'

small = Marbles(['R']*2 + ['B']*3)
large  = Marbles(['R']*20 + ['B']*30, grid=(5,10))

small_noreplace = Marbles(['R']*2 + ['B']*3)
large_noreplace  = Marbles(['R']*20 + ['B']*30, grid=(5,10))

small_noreplace.replace = False
large_noreplace.replace = False
