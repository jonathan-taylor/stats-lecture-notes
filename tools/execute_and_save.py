"""
simple example script for running notebooks and saving the resulting notebook.

Usage: `execute_and_save.py foo.ipynb [bar.ipynb [...]]`

Each cell is submitted to the kernel, and the outputs are overwritten and 
stored in new notebooks foo_executed.ipynb, etc.
"""

import os,sys,time
import base64
import re

from collections import defaultdict
from Queue import Empty

try:
    from IPython.kernel import KernelManager
except ImportError:
    from IPython.zmq.blockingkernelmanager import BlockingKernelManager as KernelManager

from IPython.nbformat.current import reads, writes, NotebookNode

def run_cell(kc, cell):
    shell = kc.shell_channel

    shell.execute(cell.input)
    # wait for finish, maximum 20s
    shell.get_msg(timeout=5)
    outs = []

    failures = 0
    while True:
        try:
            msg = shell.get_msg(timeout=5)['content']
        except Empty:
            break
        msg_type = msg['msg_type']

        if msg['status'] == 'error':
            failures += 1
            print "\nFAILURE:"
            print cell.input
            print '-----'
            print "raised:"
            print '\n'.join(msg['traceback'])
        else:
            print 'here'

        if msg_type in ('status', 'pyin'):
            print 'pyin'
            continue
        elif msg_type == 'clear_output':
            print 'clear'
            outs = []
            continue
            
        content = msg['content']
        # print msg_type, content
        out = NotebookNode(output_type=msg_type)
        
        print msg
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
                out.prompt_number = content['execution_count']
        elif msg_type == 'pyerr':
            out.ename = content['ename']
            out.evalue = content['evalue']
            out.traceback = content['traceback']
        else:
            print "unhandled iopub msg:", msg_type
        
        outs.append(out)
    return outs
    

def execute_notebook(nb):
    km = KernelManager()
    km.start_kernel(extra_arguments=['--pylab=inline'], stderr=open(os.devnull, 'w'))
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
        for cell in ws.cells:
            cell.prompt_number = prompt_number
            if cell.cell_type != 'code':
                continue
            run_cell(kc, cell)
            try:
                outs = run_cell(kc, cell)
            except Exception as e:
                print "failed to run cell:", repr(e)
                print cell.input
                errors += 1
                continue
            
            sys.stdout.write('.')
            cell.outputs = outs
            print cell.outputs
            prompt_number += 1
    km.shutdown_kernel()
    del km
    return nb

def execute_and_save(ipynb):
    with open(ipynb) as f:
        nb = reads(f.read(), 'json')
    executed_nb = execute_notebook(nb)    
    with open(ipynb.replace('.ipynb', '_executed.ipynb'), 'w') as f:
        f.write(writes(executed_nb, 'json'))


if __name__ == '__main__':
    for ipynb in sys.argv[1:]:
        print "executing %s" % ipynb
        execute_and_save(ipynb)

