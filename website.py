import os, tempfile, glob, datetime, shutil

from scripts.strip_exercises import extract_exercises
from course_modules.nbconvert.convertR import batch
from course_modules.nbconvert.convert_assignment import convert_assignment


def make_web(clean=True):

    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    
    for nbook in glob.glob('notebooks/*ipynb'):
        os.system('nbconvert.py --preamble=latex/header.tex -f latex "%s" ' % nbook)
        texfile = (os.path.splitext(nbook)[0] + '.tex')
        shutil.copy(texfile, 'notebooks/tmp.tex')
        os.system(r'cd notebooks; pdflatex "\nonstopmode\input{tmp.tex}"; mv tmp.pdf "%s"' % (os.path.basename(texfile)[:-3] + 'pdf'))

        extract_exercises([nbook], odir='exercises')
        ebook = nbook.replace('notebooks', 'exercises')
        cmd = 'nbconvert.py --preamble=latex/header.tex -f latex "%s" ' % ebook
        os.system(cmd)

        texfile = (os.path.splitext(ebook)[0] + '.tex')
        shutil.copy(texfile, 'exercises/tmp.tex')
        os.system(r'cd exercises; pdflatex "\nonstopmode\input{tmp.tex}"; mv tmp.pdf "%s"' % (os.path.basename(texfile)[:-3] + 'pdf'))

    os.system('mkdir -p  www/restricted/notebooks; cp latex/header.tex www;')
    os.system("cp notebooks/*ipynb notebooks/*pdf www/restricted/notebooks ; cd web; %s make html; cp -r _build/html/* ../www; " % cmd)

def make_pdf(clean=True):
    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    os.system("cd web; %s make latex;" % cmd)

def make_epub_book(clean=True):
    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    os.system("cd book; %s make epub;" % cmd)

def make_pdf_book(clean=True, pdf=True):
    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    os.system("cd book;  %s make latex; " % cmd)
    if pdf:
        os.system("cd book/_build/latex; make all-pdf;")

def deploy():
    os.system("rsync -avz www/* jtaylo@cardinal.stanford.edu:/afs/ir/class/stats306b/WWW")
    #os.system('''ssh jtaylo@cardinal.stanford.edu "rm -fr /afs/ir/class/stats306b/WWW/guests/* ; cp -r /afs/ir/class/stats306b/WWW/* /afs/ir/class/stats306b/WWW/guests; rm -fr /afs/ir/class/stats306b/WWW/guests/restricted/.htaccess /afs/ir/class/stats306b/WWW/guests/restricted/.htstaff" ''')
    #os.system("rm www/restricted/notes/epsdice.pdf; scp htaccess_stats306b jtaylo@cardinal.stanford.edu:/afs/ir/class/stats306b/WWW/guests/.htaccess")
