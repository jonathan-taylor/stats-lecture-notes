from PL_density import *
from conv import *

stats60_examples = {}
import dice, roulette, monty_hall
for E in [dice.examples, roulette.examples, monty_hall.examples]:
    for k in E:
        stats60_examples[k] = E[k]

from correlation import pearson_lee
from gender_bias import UCB  #, UCB_female, UCB_male

stats60_figsize = (7,7)

import matplotlib
matplotlib.rcParams['legend.scatterpoints'] = 1
matplotlib.rcParams['figure.figsize'] = (7,7)
