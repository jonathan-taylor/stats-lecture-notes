from PL_density import *
from conv import *

stats60_examples = {}
import dice, roulette, monty_hall
for E in [dice.examples, roulette.examples, monty_hall.examples]:
    for k in E:
        stats60_examples[k] = E[k]
