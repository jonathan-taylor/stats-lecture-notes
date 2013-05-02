import os, tempfile, glob, datetime, shutil

import scripts.strip_exercises as SE
reload(SE)
extract_exercises = SE.extract_exercises
from course_modules.nbconvert.convertR import batch
from course_modules.nbconvert.convert_assignment import convert_assignment


def make_web(clean=True, build_pdf=True):

    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    
    if build_pdf:
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

    os.system('mkdir -p  www/restricted/notebooks ; mkdir www/exercises ; cp latex/header.tex www;')
    os.system("cp exercises/*pdf www/exercises; cp notebooks/*ipynb notebooks/*pdf www/restricted/notebooks ; cd web; %s;  make html; cp -r _build/html/* ../www; ")

def deploy():
    os.system("rsync -avz www/* jtaylo@cardinal.stanford.edu:/afs/ir/class/stats306b/WWW")

