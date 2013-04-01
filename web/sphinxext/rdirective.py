import sys, os, cStringIO
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from docutils.parsers.rst import directives
from rrunner import shell
import time, codecs
deltat = 0.01

# print R output to console?
debug = False

def rplot_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):

    if len(arguments) == 1: # it is a filename
        content = [file(arguments[0]).read()]

    m = md5()
    contentstr = '\n'.join([c for c in content])
    m.update(contentstr)
    hash = m.hexdigest()[-10:]

    if not os.path.exists("images/inline"):
        response = ''
        while response not in ['Y', 'N']:
            print 'Directory %s does not exist, Create [Y/N]?' % os.path.abspath('images/inline')
            response = raw_input().strip().upper()
        if response == 'Y':
            os.makedirs('images/inline')
            
    shell.process('png("images/inline/%s.png", width=600, height=600)' % hash, echo=False)
    shell.astext() # flush

    force = options.pop('force', False) # if present in options, force is None
    caption = options.pop('caption', None)

    if not os.path.exists("images/inline/%s.Routput" % hash) or force is None:
        if debug:
            ll = '\n' + '-'*50 + '\n'
            sys.stderr.write(ll + 'working on rplot:' + ll + contentstr + ll)

        shell.process(contentstr, echo=True)
        time.sleep(deltat)

        output = shell.astext().split('\n')
        codecs.open("images/inline/%s.Routput" % hash, 'w', 'utf-8').write('\n'.join(output))
        if debug:
            sys.stderr.write(('output file: images/inline/%s.Routput\n' % hash) +
                         file("images/inline/%s.Routput" % hash).read())
    else:
        output = codecs.open("images/inline/%s.Routput" % hash, 'r', 'utf-8').read().split('\n') 
        shell.input += "%s\n" % contentstr

    if debug:
        print 'RPLOT CONTENT', content
        print 'RPLOT OUTPUT', output
    
    shell.process('dev.off()', echo=False)

    shell.astext() # flush

    silent = False
    if options.pop('silent', False) is None:
        silent = True
        
    if options.pop('source', False) is None: # if present in options,
                                             # source is None
        lines = content
    else:
        lines = output

    # flush R specific options before creating fig options
    for k in ['force', 'silent', 'caption', 'source']:
        options.pop(k, None)
        
    fig_options = ["   :%s: %s" % (k,v) for (k, v) in options.items()]

    if len(lines) and not silent:
        r_lines = ['.. code-block:: r', '']
        r_lines.extend([u'    %s'% line for line in lines])
        r_lines.extend(['.. figure:: images/inline/%s.png' % hash] +
                       fig_options + [''])
        if caption:
            r_lines.extend(['    %s' % caption, ''])
            

        state_machine.insert_input(
            r_lines, state_machine.input_lines.source(0))

    return []

def rcode_directive(name, arguments, options, content, lineno,
                   content_offset, block_text, state, state_machine):

    if len(arguments) == 1: # it is a filename
        content = [file(arguments[0]).read()]

    shell.astext()

    contentstr = '\n'.join([c for c in content])

    m = md5()
    m.update(contentstr)
    hash = m.hexdigest()[-10:]

    force = options.pop('force', False) # if present in options, force is None

    if not os.path.exists("images/inline/%s.Routput" % hash) or force is None:
        if debug:
            ll = '\n' + '-'*50 + '\n'
            sys.stderr.write(ll + 'working on rcode:' + ll + contentstr + ll)
        shell.process(contentstr, echo=True)
        time.sleep(deltat)
        output = shell.astext().split('\n')
        codecs.open("images/inline/%s.Routput" % hash, 'w', 'utf-8').write('\n'.join(output))
        if debug:
            sys.stderr.write(('output file: images/inline/%s.Routput\n' % hash) +
                             file("images/inline/%s.Routput" % hash).read())
    else:
        output = codecs.open("images/inline/%s.Routput" % hash, 'r', 'utf-8').read().split('\n') 
        shell.input += "%s\n" % contentstr

    if debug:
        print 'RCODE CONTENT', content
        print 'RCODE OUTPUT', output

    silent = False
    if options.pop('silent', False) is None:
        silent = True
        
    if options.pop('source', False) is None: # if present in options,
                                             # source is None
        lines = content
    else:
        lines = output

    if len(lines) and not silent:
        r_lines = ['.. code-block:: r', '']
        r_lines.extend([u'    %s'%line for line in lines])
        r_lines.append('')

        state_machine.insert_input(
            r_lines, state_machine.input_lines.source(0))

    return []


def rflush_directive(name, arguments, options, content, lineno,
                     content_offset, block_text, state, state_machine):

    silent = False
    if options.pop('silent', False) is None:
        silent = True
        
    lines = shell.flush_input().split("\n")
    if debug:
        print 'RFLUSH LINES', lines
    
    if len(lines) and not silent:
        r_lines = ['R code for cut and paste',
                   '--------------------------',
                   '']
        r_lines += ['.. code-block:: r', '']
        r_lines.extend([u'    %s'%line for line in lines])
        r_lines.append('')

        state_machine.insert_input(
            r_lines, state_machine.input_lines.source(0))

    return []

options = {'silent':directives.flag,
           'source':directives.flag,
           'force':directives.flag,
           'caption':directives.unchanged,
           'height':directives.unchanged,
           'width':directives.unchanged,
           'scale':directives.unchanged,
           'alt':directives.unchanged,
           'align':directives.unchanged}

def setup(app):
    setup.app = app
    app.add_directive('rplot', rplot_directive, True, (0, 2, 0), **options)
    app.add_directive('rcode', rcode_directive, True, (0, 2, 0), **options)
    app.add_directive('rflush', rflush_directive, True, (0, 2, 0), **options)    


