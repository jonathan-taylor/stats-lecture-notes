import os
from md5 import md5
from ipython_directive import shell
from docutils.parsers.rst import directives

import matplotlib.mlab as ML
from rec2csv_pretty import rec2csv_pretty

def rectable_directive(name, arguments, options, content, lineno,
                       content_offset, block_text, state, state_machine):

    for line in content:
        shell.process(line)

    content = '\n'.join(content)
    if options.has_key('variable'):
        variable = options['variable']
    else:
        raise ValueError('must specify a variable name with the "variable" option')

    outdir = os.path.join("build", "table_directive", "inline")
    try:
        os.makedirs(outdir)
    except OSError:
        pass

    fname = os.path.join(outdir, md5(content).hexdigest()[-10:] + ".csv")

    shell.process("import matplotlib.mlab as ML; ML.rec2csv(%s, '%s')" %
                  (variable, fname))
    newfname = os.path.join(outdir, md5(file(fname).read()).hexdigest()[-10:] + '.csv')
    os.rename(fname, newfname)

    if options.has_key('pretty'):
        rec = ML.csv2rec(newfname)
        rec2csv_pretty(rec, newfname, overwrite_float_precision=False)

    lines = shell.astext().split('\n')
    if len(lines):
        ipy_lines = ['.. csv-table::', '    :file: %s' % newfname, '']
        #ipy_lines.extend(['    %s'%line for line in lines])
        ipy_lines.append('')

        state_machine.insert_input(
            ipy_lines, state_machine.input_lines.source(0))

    return []

def setup(app):
    setup.app = app
    options = {}
    app.add_directive('rectable', rectable_directive, True, (0, 2, 0),
                      variable=directives.unicode_code,
                      pretty=directives.flag)
