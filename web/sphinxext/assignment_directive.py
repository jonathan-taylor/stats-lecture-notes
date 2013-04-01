import sys, os, cStringIO
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from docutils.parsers.rst import directives
from rrunner import shell

import os, shutil, tempfile
import enthought.traits.api as traits

######################################################

HOMEDIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
ASSDIR = "%s/assignments" % HOMEDIR
QUIZDIR = "%s/quizzes" % HOMEDIR

# class Assignment(traits.HasTraits):

#     pdf = traits.false
#     solution = traits.false
#     number = traits.Int

#     def build_pdf(self):
#         bdir = os.path.abspath(os.path.join(ASSPATH, '..'))
#         adir = os.path.join(bdir, 'assignments', 'assignment%d' % self.number)
#         cmd = """
#         cd %(adir)s;
#         pdflatex assignment%(num)d.tex;
#         pdflatex assignment%(num)d.tex;
#         rm assignment%(num)d.aux ; 
#         rm assignment%(num)d.log ; 
#         rm assignment%(num)d.out ; 
#         mkdir -p %(bdir)s/www_new/restricted;
#         cp assignment%(num)d.pdf %(bdir)s/www_new/restricted;
#         """ % {'bdir':bdir, 'adir':adir, 'num':self.number}
#         print cmd
#         os.system(cmd)

#     def build_solution(self, killtmp=False):
#         bdir = os.path.abspath(os.path.join(ASSPATH, '..'))
#         adir = os.path.join(bdir, 'assignments', 'assignment%d' % self.number)
        
#         cdir = os.path.abspath(os.curdir)
#         os.chdir(adir)
#         if os.path.exists("solution%d.Rnw" % self.number):
#             tdir = tempfile.mkdtemp()
#             os.system("cp solution%d.Rnw %s" % (self.number, tdir))
#             os.chdir(tdir)
#             import rpy
#             rpy.r('Sweave("solution%d.Rnw")' % self.number)
        
#         cmd = """
#         chdir %(tdir)s;
#         pdflatex solution%(num)d.tex;
#         pdflatex solution%(num)d.tex;
#         mkdir -p %(bdir)s/www_new/restricted;
#         cp solution%(num)d.pdf %(bdir)s/www_new/restricted;
#         """ % {'bdir':bdir, 'tdir':tdir, 'num':self.number}

#         os.system("cp %s/solution%d.pdf %s" % (tdir, self.number, adir))
#         if killtmp:
#             shutil.rmtree(tdir)
#         os.chdir(cdir)
#         print cmd
#         os.system(cmd)
                  
#     def __init__(self, number):
#         self.number = number

################################################

def assignment_directive(name, arguments, options, content, lineno,
                         content_offset, block_text, state, state_machine):

    assigned = options['assigned']
    solved = options['solved']

    if assigned:
        assigned = [int(a) for a in options['assigned'].split(',')]
    else:
        assigned = []

    if solved:
        solved = [int(s) for s in options['solved'].split(',')]
    else:
        solved = []

    lines = ['Assignments', '-----------', '']

    assignments = []
    for a in sorted(assigned):
        os.system('cp %s/assignment%d/assignment%d.pdf %s/www/restricted' % (ASSDIR, int(a), int(a), HOMEDIR))
        if a in solved:
            os.system('cp %s/assignment%d/assignment%d_solution.pdf %s/www/restricted' % (ASSDIR, int(a), int(a), HOMEDIR))
            lines += ['* `Assignment %(a)d <restricted/assignment%(a)d.pdf>`_, `Solution <restricted/assignment%(a)d_solution.pdf>`_' % {'a':int(a)}, '']
        else:
            lines += ['* `Assignment %(a)d <restricted/assignment%(a)d.pdf>`_' % {'a':int(a)}, '']

    lines += ['']
    
    state_machine.insert_input(
        lines, state_machine.input_lines.source(0))

    return []

def practice_quiz_directive(name, arguments, options, content, lineno,
                            content_offset, block_text, state, state_machine):

    assigned = options['assigned']
    solved = options['solved']

    if assigned:
        assigned = [int(a) for a in options['assigned'].split(',')]
    else:
        assigned = []

    if solved:
        solved = [int(s) for s in options['solved'].split(',')]
    else:
        solved = []

    lines = ['Practice quizzes', '-----------------', '']

    practice_quizzes = []
    for a in sorted(assigned):
        os.system('cp %s/practice%d/practice%d.pdf %s/www/restricted' % (QUIZDIR, int(a), int(a), HOMEDIR))

        if a in solved:
            os.system('cp %s/practice%d/practice%d_solution.pdf %s/www/restricted' % (QUIZDIR, int(a), int(a), HOMEDIR))
            lines += ['* `Practice Quiz %(a)d <restricted/practice%(a)d.pdf>`_, `Solution <restricted/practice%(a)d_solution.pdf>`_' % {'a':int(a)}, '']
        else:
            lines += ['* `Practice Quiz %(a)d <restricted/practice%(a)d.pdf>`_' % {'a':int(a)}, '']


    lines += ['']
    
    state_machine.insert_input(
        lines, state_machine.input_lines.source(0))

    return []

def solved_quiz_directive(name, arguments, options, content, lineno,
                            content_offset, block_text, state, state_machine):

    solved = options['solved']

    if solved:
        solved = [int(s) for s in options['solved'].split(',')]
    else:
        solved = []

    lines = ['Quiz solutions', '-------------------', '']

    practice_quizzes = []
    for a in sorted(solved):
        os.system('cp %s/quiz%d/quiz%d_solution.pdf %s/www/restricted' % (QUIZDIR, int(a), int(a), HOMEDIR))
        lines += ['* `Solved Quiz %(a)d <restricted/quiz%(a)d_solution.pdf>`_' % {'a':int(a)}, '']


    lines += ['']
    
    state_machine.insert_input(
        lines, state_machine.input_lines.source(0))

    return []


options = {'assigned': directives.unchanged,
           'solved': directives.unchanged}
           

def setup(app):
    setup.app = app
    app.add_directive('assignments', assignment_directive, True, (0, 0, 0), **options)
    app.add_directive('practice_quizzes', practice_quiz_directive, True, (0, 0, 0), **options)
    app.add_directive('solved_quizzes', solved_quiz_directive, True, (0, 0, 0), **options)



