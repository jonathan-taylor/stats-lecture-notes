'''
Some functions used in publishing notebooks
'''

import os, sys

from Queue import Empty

try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, NotebookNode, writes

def run_cell(kc, cell, collect_outputs=True):
    """
    Run contents of a cell in a kernel client.
    If collect_outputs is True, return the outputs as a list.
    """
    shell = kc.shell_channel
    iopub = kc.iopub_channel
    outputs = []

    shell.execute(cell.input)
    # wait for finish, maximum 20s
    try:
        shell.get_msg(timeout=10)
    except Empty:
        return []

    if collect_outputs:
        outputs = []
        while True:
            try:
                reply = iopub.get_msg(timeout=0.2)
            except Empty:
                break
            content = reply['content']
            msg_type = reply['msg_type']

            if msg_type in ('status', 'pyin'):
                continue
            elif msg_type == 'clear_output':
                outputs = []
                continue

            out = NotebookNode(output_type=msg_type)

            if msg_type == 'stream':
                out.stream = content['name']
                out.text = content['data']
            elif msg_type in ('display_data', 'pyout'):
                for mime, data in content['data'].iteritems():
                    attr = mime.split('/')[-1].lower()
                    # this gets most right, but fix svg+html, plain
                    attr = attr.replace('+xml', '').replace('plain', 'text')
                    setattr(out, attr, data)
                if msg_type == 'pyout':
                    out.prompt_number = cell.prompt_number
            elif msg_type == 'pyerr':
                out.ename = content['ename']
                out.evalue = content['evalue']
                out.traceback = content['traceback']
            else:
                print "unhandled iopub msg:", msg_type

            outputs.append(out)
        return outputs
    return []

def run_notebook(nb, cell_filter = lambda cell: cell,
                 extra_arguments=['--pylab=inline', '--profile=stats'],
                 modify_outputs=True):
    """
    Take a notebook and send all its cells to a kernel.
    Takes an optional filter to modify the results of the 
    cell after being run and having its 
    output set by `run_cell` if modify_outputs is True.
    """
    km = KernelManager()
    km.start_kernel(extra_arguments=extra_arguments, 
                    stderr=open(os.devnull, 'w'))
    try:
        kc = km.client()
    except AttributeError:
        # 0.13
        kc = km
    kc.start_channels()
    shell = kc.shell_channel

    shell.execute("pass")
    shell.get_msg()

    successes = 0
    failures = 0
    errors = 0
    prompt_number = 1
    for ws in nb.worksheets:
        new_cells = []
        for cell in ws.cells:
            cell.prompt_number = prompt_number

            if cell['cell_type'] != 'code':
                new_cells.append(cell)
                continue

            outs = run_cell(kc, cell, 
                            collect_outputs=modify_outputs)
            try:
                outs = run_cell(kc, cell, 
                                collect_outputs=modify_outputs)
            except Exception as e:
                print "failed to run cell:", repr(e)
                print cell.input
                errors += 1
                continue

            sys.stdout.write('.')
            if modify_outputs:
                cell.outputs = outs
            new_cell = cell_filter(cell)
            if new_cell is not None:
                new_cells.append(new_cell)
            prompt_number += 1
        ws.cells = new_cells
    km.shutdown_kernel()
    del km
    return nb

def strip_outputs(nb,
                  extra_arguments=['--pylab=inline', '--profile=stats']): 
    """
    Take a notebook, run each cell and strip all of its outputs
    """
    def _strip(cell):
        cell.outputs = []
    return run_notebook(nb, cell_filter=_strip,
                        extra_arguments=extra_arguments,
                        modify_outputs=False)

def strip_skipped_cells(nb,
                  extra_arguments=['--pylab=inline', '--profile=stats']): 
    """
    Take a notebook, run each cell and strip all of its outputs
    """
    def _strip_skip(cell):
        try:
            if cell['metadata']['slideshow']['slide_type'] == 'skip':
                return None
            else:
                return cell
        except KeyError:
            return cell

    return run_notebook(nb, cell_filter=_strip_skip,
                        extra_arguments=extra_arguments,
                        modify_outputs=False)

def load(ipynb, format='json'):
    """
    load a notebook
    """
    with open(ipynb, 'r') as f:
        nb = reads(f.read(), 'json')
    return nb
