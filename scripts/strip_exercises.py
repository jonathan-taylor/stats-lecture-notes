#!/usr/bin/env python

"""
Clear everything but exercises from an IPython notebook.

Exercises are defined in the metadata.
By default, it prints the notebooks without outputs into stdout.

"""

import sys, os
from copy import copy

from IPython.nbformat import current as nbformat


def clear_everything_but_exercises(nb):
    """Clear output of notebook `nb` INPLACE."""
    for ws in nb.worksheets:
        keep_cells = []
        header = copy(ws.cells[0])
        header.cell_type = 'heading'
        header.level = 1
        header.source = r'Exercises: %s' % nb['metadata']['name'].replace('_', ' ')

        for cell in ws.cells:
            if 'metadata' in cell and 'exercise' in cell['metadata']:
                keep_cells.append(cell)
            else:
                if hasattr(cell, 'source'):
                    cell.source = []
                if hasattr(cell, 'input'):
                    cell.input = []
                cell.outputs = []
        ws.cells = [header] + keep_cells
    return nb

def extract_exercises(inputs, odir='exercises', inplace=False):
    """
    Strip output of notebooks.

    Parameters
    ----------
    inputs : list of string
        Path to the notebooks to be processed.
    inplace : bool
        If this is `True`, outputs in the input files will be deleted.
        Default is `False`.

    """
    for inpath in inputs:
        with file(inpath) as fp:
            nb = nbformat.read(fp, 'ipynb')
        clear_everything_but_exercises(nb)
        if odir:
            nbformat.write(nb, file(os.path.join(odir, os.path.basename(inpath)), 'w'), 'ipynb')

def main():
    from argparse import ArgumentParser
    parser = ArgumentParser(description=__doc__)
    parser.add_argument('inputs', nargs='+', metavar='input',
                        help='Paths to notebook files.')
    args = parser.parse_args()
    extract_exercises(**vars(args))

if __name__ == '__main__':
    main()
