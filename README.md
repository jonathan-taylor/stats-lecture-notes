STATS 306B / 191 Notebooks
==========================

This repo collects course material for STATS306B and STATS191,
taught by Jonathan Taylor at Stanford.

The notebooks presume you are running in a certain ipython profile
which is setup in ./profile_stats.

To check dependencies, and install this profile, run:

`python check_install.py`

from the terminal. This will, among other things, copy the `profile_stats`
folder to your `~/.ipython` directory, to give you an ipython profile called
`stats`

To run the notebooks, change directory to the folder containing the notebooks
and run `ipython notebook --profile=stats` from the command line.

knitr magic
-----------

Besides a custom .css, the `stats` ipython profile provides a new cell_magic
`%%knitr` which produces `R` output as if run through `knitr`.
