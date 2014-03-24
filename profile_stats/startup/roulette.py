from matplotlib.patches import Circle, Rectangle
import matplotlib.pyplot as plt
import numpy as np
from base64 import encodestring
import PIL.Image
from IPython.core.pylabtools import print_figure
from IPython.core.display import HTML

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
                bg_alpha=None
                ):
    fig = plt.figure(figsize=(4,4))
    ax = fig.gca()
    circle = Circle((0,0), 1., facecolor=facecolor,
                    edgecolor='k')
    ax.add_patch(circle)
    ax.text(0, 0, s,
            horizontalalignment='center',
            verticalalignment='center', 
            fontsize=fontsize,
            color='white')
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

for k in _colors:
    if k not in _places_cache:
        _places_cache[k] = _html_place(k, 
                                       facecolor=_colors[k])

def roulette_table(colors={}, alpha=0.5):

    """
    Return a table of all 36 possible
    values for a pair of roulette.

    Parameters
    ----------

   colors : {}
        Dict indexed by place labels which
        determine what color to label this
        outcome.

    alpha : float
        Used in roulette_html to blend all colors.

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
            if place in colors:
                if (place, colors[place], alpha) not in _places_cache:
                    _places_cache[(place, colors[place], alpha)] = \
                        _html_place(place, 
                                    facecolor=_colors[place],
                                    bg_alpha=(colors[place], alpha))
                roulette_row += '<td>' + _places_cache[(place, colors[place], alpha)] + '</td>'
            else:
                roulette_row += '<td>' + _places_cache[place] + '</td>'
        roulette_row += '</tr>'
        roulette_str += roulette_row + '\n'
    return roulette_str + '</table>\n'

def roulette_trial(testfn = lambda i : i % 2 == 1, # odd by default
                   outcome=None, color="#0000aa", alpha=0.25,
                   success='#00aa00',
                   failure='#aa0000'):
    """
    roulette_table with all outcomes who evaluate to true by `testfn`
    colored `color`

    Parameters
    ----------

    outcome : (int, int) [optional]
        Outcome of rolling the roulette.
    
    color : color 
        Color to label those that pass testfn
    """
    colors = {}
    for place in range(1,37):
        if testfn(place):
            colors[place] = color

    if outcome is not None:
        if outcome in colors:
            colors[outcome] = success
        else:
            colors[outcome] = failure

    return roulette_table(colors, alpha=alpha)
