import os, tempfile, glob, datetime, shutil

from course_modules.nbconvert.convertR import batch
from course_modules.nbconvert.convert_assignment import convert_assignment

def collect_slides(outrst, heading, *rstfiles):
    o = file('slides/%s' % outrst, 'w')
    o.write('.. s306b_preamble::\n')
    o.write('   :title: %s\n\n' % heading)
    for rstfile in rstfiles:
        raw = file("slides/%s" % rstfile).read()
        raw = raw.replace('s306b_preamble', 's306b_part')
        raw = raw.replace('.. closing::', '')
        o.write(raw)
    o.write('\n'.join(['.. closing::', '   :noblank:','','','']))
    o.close()

def make_slides(rstfile, delete_tmp=True):
    tmpd = tempfile.mkdtemp()
    bdir = os.path.abspath(os.path.dirname(__file__))
    base = os.path.basename(rstfile)[:-4]
    vals = {'nbk':'%s/notebooks',
            'slides':'%s/slides' % bdir,
            'web':'%s/web' % bdir,
            'www':'%s/www' % bdir,
            'tmp':tmpd,
            'rstfile':rstfile,
            'txtfile':rstfile[:-3] + 'txt',
            'texfile':rstfile[:-3] + 'tex',
            'pdffile':rstfile[:-3] + 'pdf',
            'tex':"%s/tex" % bdir,
            'base':base,
            'data':'%s/data' % bdir,
            'images':'%s/notes/built/images' % bdir}

    cmd = r'''
    cp %(slides)s/../notes/image.png %(tex)s/* %(tmp)s;
    cd %(slides)s; cp -r %(rstfile)s figs index.rst conf.py sphinxext %(tmp)s;
    cp -r %(data)s %(tmp)s;
    mkdir -p %(images)s;
    ln -s %(images)s %(tmp)s/images;
    cp -r %(slides)s/../python/*py %(tmp)s;
    cp %(web)s/sphinxext/r*py %(tmp)s/sphinxext ; 
    cd %(tmp)s ; rm -fr _build/text
    rm `find . -name \*pyc`
    sphinx-build -E -P -b text -d _build/doctrees . _build/text;
    mkdir %(www)s/restricted/notebooks;
    cp %(nbk)/*ipynb %(www)s/restricted/notebooks;
    cp _build/text/%(txtfile)s %(texfile)s;
    pdflatex "\nonstopmode\input{%(texfile)s}";
    killall -9 R ;
    mkdir -p %(slides)s/../notes/built/images/inline;
    mkdir -p %(slides)s/../notes/built/figs;
    cp %(texfile)s  %(slides)s/../notes/built;
    cp -r figs/* %(slides)s/../notes/built/figs ; 
    mkdir -p %(www)s/restricted/notes ;
    cp *pdf %(www)s/restricted/notes ;
    cd %(www)s/restricted/notes;
    ''' % vals  

    update_images(tmpd, "%s/notes/built/images/inline" % bdir)

    print cmd
    os.system(cmd)

    if delete_tmp:
        os.system('rm -fr %s' % tmpd)
    else:
        print cmd
        print tmpd

def update_images(ind, outd):
    for f in glob.glob('%s/*' % ind):
        if not os.path.exists("%s/%s" % (outd, os.path.split(f)[1])):
            os.system('cp %s %s' % (f, outd))
            print f

due_date = {1:(2011,10,6),
            2:(2011,10,20),
            3:(2011,11,4),
            4:(2011,11,18),
            5:(2011,12,13)}


def make_assignment(assignment_num, date=None):
    assignment_dir = os.path.abspath("assignments/assignment%d" % assignment_num)
    convert_assignment("%s/assignment%d.ipynb" % (assignment_dir, assignment_num), '', date, assignment_num,
                       preamble=preamble_306b)

    cmd = r"""
    cd %(dir)s; pdflatex "\nonstopmode\input{assignment%(num)d.tex}";
    pdflatex "\nonstopmode\input{assignment%(num)d.tex}";
    rm assignment%(num)d.log assignment%(num)d.aux assignment%(num)d.out 

    """ % {'dir':assignment_dir, 'num':assignment_num}
    os.system(cmd)

   

def make_midterm(date=datetime.date(2011,11,2), delete_tmp=True):
    quiz_dir = os.path.abspath("quizzes/midterm")
    tmpd = tempfile.mkdtemp()
    bdir = os.path.abspath(os.path.dirname(__file__))
    vals = {'tex':"%s/tex" % bdir,
            'quiz':quiz_dir,
            'web':'%s/web' % bdir,
            'www':'%s/www' % bdir,
            'tmp':tmpd,
            'data':'%s/data' % bdir,
            'images':'%s/notes/built/images' % bdir}

    cmd = r'''
    cp %(quiz)s/../../notes/image.png %(tex)s/* %(tmp)s;
    cd %(quiz)s; cp -r *rst *csv ../conf.py ../sphinxext %(tmp)s;
    cp -r %(data)s %(tmp)s;
    mkdir -p %(images)s;
    ln -s %(images)s %(tmp)s/images;
    cp -r %(quiz)s/../../python/*py %(tmp)s;
    cp %(web)s/sphinxext/r*py %(tmp)s/sphinxext ; 
    cd %(tmp)s ; rm -fr _build/text
    rm `find . -name \*pyc`
    sphinx-build -E -P -b text -d _build/doctrees . _build/text
    cp _build/text/*txt %(quiz)s;
    cp -r images %(quiz)s;
    ''' % vals  

    print cmd
    os.system(cmd)

    template = r"""
    \documentclass{article}

    \usepackage{graphicx} 
    \usepackage[colorlinks=true,
                linkcolor=blue,
                citecolor=blue,
                urlcolor=blue,
                ]{hyperref}

    \usepackage{graphicx}
    \usepackage{amsmath,amssymb}
    \usepackage{color}

    \newcommand{\coursedir}{http://stats306b.stanford.edu}
    \newcommand{\R}{\href{http://cran.r-project.org}{R}}

    \renewcommand{\theenumi}{\arabic{enumi}}
    \renewcommand{\labelenumi}{Q. \theenumi)}
    \renewcommand{\theenumii}{\alph{enumii}}
    \renewcommand{\labelenumii}{(\theenumii)}

    \newcommand{\homeurl}{http://stats306b.stanford.edu}

    \begin{document}

    \title{Statistics 306b \\ Fall 2011 \\ Data Mining \\ Midterm \\ Date: %(date)s}
    \author{Prof. J.  Taylor}
    \date{}
    \maketitle 

    %(special)s 

    \begin{enumerate}

    %(questions)s

    \end{enumerate}

    \end{document}
    """

    if date is None:
        datestr = 'TBA'
    else:
        if not isinstance(date, datetime.date):
            y, m, d = date
            datet = datetime.date(y,m,d)
        else:
            datet = date
        datestr = datet.strftime("%A %B %d, %Y")

    questions = '\n\n'.join(['\item %s' % file(f).read() for f in sorted(glob.glob("%s/q*txt" % quiz_dir))])


    texstr = template % {'questions':questions,
                         #'num': quiz_num,
                         'date':datestr,
                         'special':file("%s/index.rst" % quiz_dir).read()}

    file("%s/midterm.tex" % (quiz_dir), 'w').write(texstr)
    cmd = r"""
    cd %(dir)s; pdflatex "\nonstopmode\input{midterm.tex}" &> tex.log;
    pdflatex "\nonstopmode\input{midterm.tex}" &> tex.log ;
    rm midterm.log midterm.aux midterm.out;
    killall -9 R
    """ % {'dir':quiz_dir}#}, 'num':quiz_num}
    os.system(cmd)

    if delete_tmp:
        os.system('rm -fr %s' % tmpd)
    else:
        print tmpd

def make_exam(date=datetime.date(2011,12,12), delete_tmp=True):
    quiz_dir = os.path.abspath("quizzes/exam")
    tmpd = tempfile.mkdtemp()
    bdir = os.path.abspath(os.path.dirname(__file__))
    vals = {'tex':"%s/tex" % bdir,
            'quiz':quiz_dir,
            'web':'%s/web' % bdir,
            'www':'%s/www' % bdir,
            'tmp':tmpd,
            'data':'%s/data' % bdir,
            'images':'%s/notes/built/images' % bdir}

    cmd = r'''
    cp %(quiz)s/../../notes/image.png %(tex)s/* %(tmp)s;
    cd %(quiz)s; cp -r *rst *csv ../conf.py ../sphinxext %(tmp)s;
    cp -r %(data)s %(tmp)s;
    mkdir -p %(images)s;
    ln -s %(images)s %(tmp)s/images;
    cp -r %(quiz)s/../../python/*py %(tmp)s;
    cp %(web)s/sphinxext/r*py %(tmp)s/sphinxext ; 
    cd %(tmp)s ; rm -fr _build/text
    rm `find . -name \*pyc`
    sphinx-build -E -P -b text -d _build/doctrees . _build/text
    cp _build/text/*txt %(quiz)s;
    cp -r images %(quiz)s;
    ''' % vals  

    print cmd
    os.system(cmd)

    template = r"""
    \documentclass{article}

    \usepackage{graphicx} 
    \usepackage[colorlinks=true,
                linkcolor=blue,
                citecolor=blue,
                urlcolor=blue,
                ]{hyperref}

    \usepackage{graphicx}
    \usepackage{amsmath,amssymb}
    \usepackage{color}

    \newcommand{\coursedir}{http://stats306b.stanford.edu}
    \newcommand{\R}{\href{http://cran.r-project.org}{R}}

    \renewcommand{\theenumi}{\arabic{enumi}}
    \renewcommand{\labelenumi}{Q. \theenumi)}
    \renewcommand{\theenumii}{\alph{enumii}}
    \renewcommand{\labelenumii}{(\theenumii)}

    \newcommand{\homeurl}{http://stats306b.stanford.edu}

    \begin{document}

    \title{Statistics 306b \\ Fall 2011 \\ Data Mining \\ Final Exam \\ Date: %(date)s}
    \author{Prof. J.  Taylor}
    \date{}
    \maketitle 

    %(special)s 

    \begin{enumerate}

    %(questions)s

    \end{enumerate}

    \end{document}
    """

    if date is None:
        datestr = 'TBA'
    else:
        if not isinstance(date, datetime.date):
            y, m, d = date
            datet = datetime.date(y,m,d)
        else:
            datet = date
        datestr = datet.strftime("%A %B %d, %Y")

    questions = '\n\n'.join(['\item %s' % file(f).read() for f in sorted(glob.glob("%s/q*txt" % quiz_dir))])


    texstr = template % {'questions':questions,
                         #'num': quiz_num,
                         'date':datestr,
                         'special':file("%s/index.rst" % quiz_dir).read()}

    file("%s/exam.tex" % (quiz_dir), 'w').write(texstr)
    cmd = r"""
    cd %(dir)s; pdflatex "\nonstopmode\input{exam.tex}" &> tex.log;
    pdflatex "\nonstopmode\input{exam.tex}" &> tex.log ;
    rm exam.log exam.aux exam.out;
    killall -9 R
    """ % {'dir':quiz_dir}#}, 'num':quiz_num}
    os.system(cmd)

    if delete_tmp:
        os.system('rm -fr %s' % tmpd)
    else:
        print tmpd

def make_practice_quiz(practice_num, date=None, delete_tmp=True):
    practice_dir = os.path.abspath("quizzes/practice%d" % practice_num)
    tmpd = tempfile.mkdtemp()
    bdir = os.path.abspath(os.path.dirname(__file__))
    vals = {'tex':"%s/tex" % bdir,
            'practice':practice_dir,
            'web':'%s/web' % bdir,
            'www':'%s/www' % bdir,
            'tmp':tmpd}

    cmd = r'''
    cp %(practice)s/../../notes/image.png %(tex)s/* %(tmp)s;
    cd %(practice)s; cp -r *rst *csv ../conf.py ../sphinxext %(tmp)s;
    cp -r %(practice)s/../../python/*py %(tmp)s;
    cp %(web)s/sphinxext/r*py %(tmp)s/sphinxext ; 
    cd %(tmp)s ; rm -fr _build/text
    rm `find . -name \*pyc`
    sphinx-build -E -P -b text -d _build/doctrees . _build/text
    cp _build/text/*txt %(practice)s;
    cp -r images %(practice)s;
    ''' % vals  

    print cmd
    os.system(cmd)

    template = r"""
    \documentclass{article}

    \usepackage{graphicx} 
    \usepackage[colorlinks=true,
                linkcolor=blue,
                citecolor=blue,
                urlcolor=blue,
                ]{hyperref}

    \usepackage{graphicx}
    \usepackage{amsmath,amssymb}
    \usepackage{color}

    \newcommand{\coursedir}{http://stats306b.stanford.edu}
    \newcommand{\R}{\href{http://cran.r-project.org}{R}}

    \renewcommand{\theenumi}{\arabic{enumi}}
    \renewcommand{\labelenumi}{Q. \theenumi)}
    \renewcommand{\theenumii}{\alph{enumii}}
    \renewcommand{\labelenumii}{(\theenumii)}

    \newcommand{\homeurl}{http://stats306b.stanford.edu}

    \begin{document}

    \title{Statistics 306b \\ Fall 2011 \\ Data Mining \\ Practice Quiz \#%(num)d }
    \author{Prof. J.  Taylor}
    \date{}
    \maketitle 

    %(special)s 

    \begin{enumerate}

    %(questions)s

    \end{enumerate}

    \end{document}
    """

    if date is None:
        datestr = 'TBA'
    else:
        if not isinstance(date, datetime.date):
            y, m, d = date
            datet = datetime.date(y,m,d)
        else:
            datet = date
        datestr = datet.strftime("%A %B %d, %Y")

    questions = '\n\n'.join(['\item %s' % file(f).read() for f in sorted(glob.glob("%s/q*txt" % practice_dir))])


    texstr = template % {'questions':questions,
                         'num': practice_num,
                         'date':datestr,
                         'special':file("%s/index.rst" % practice_dir).read()}

    file("%s/practice%d.tex" % (practice_dir, practice_num), 'w').write(texstr)
    cmd = r"""
    cd %(dir)s; pdflatex "\nonstopmode\input{practice%(num)d.tex}" &> tex.log;
    pdflatex "\nonstopmode\input{practice%(num)d.tex}" &> tex.log;
    rm practice%(num)d.log practice%(num)d.aux practice%(num)d.out question*txt index.txt;
    killall -9 R
    """ % {'dir':practice_dir, 'num':practice_num}
    os.system(cmd)

    if delete_tmp:
        os.system('rm -fr %s' % tmpd)
    else:
        print tmpd
    
first_tuesday = (2011,3,29)
def tuesday(i):
    week = datetime.date(2011,4,11)-datetime.date(2011,4,4)
    date = datetime.date(*first_tuesday)
    for _ in range(i):
        date += week
    return date

first_friday = (2011,4,1)
def friday(i):
    week = datetime.date(2011,4,11)-datetime.date(2011,4,4)
    date = datetime.date(*first_friday)
    for _ in range(i):
        date += week
    return date


def make_all_assignments(first=first_friday, delete_tmp=True):
    week = datetime.date(2011,4,11)-datetime.date(2011,4,4)
    date = datetime.date(*first)
    for i in range(9):
        make_assignment(i+1, date, delete_tmp=delete_tmp)
        date += week

def make_all_slides(first=first_friday, delete_tmp=True):
    week = datetime.date(2011,4,11)-datetime.date(2011,4,4)
    date = datetime.date(*first)
    for i in range(9):
        make_assignment(i+1, date, delete_tmp=delete_tmp)
        date += week



def make_week(i, slides):#, quiz=True, practice=True, assignment=True):
    if slides:
        for slide in slides:
            make_slides(slide)
        collect_slides('week%d.rst' % i, 'Week %d' % i, *slides)
        make_slides('week%d.rst' % i)
        os.system('cd www/restricted/notes; pdfnup --nup 2x2  week%d.pdf; mv week%d-*.pdf week%d_2x2.pdf' % (i,i,i))

    ## if assignment:
    ##     _friday = friday(i-1)
    ##     make_assignment(i, _friday)

    ## if quiz:
    ##     _tuesday = tuesday(i)
    ##     make_quiz(i, _tuesday)
    ## if practice:
    ##     make_practice_quiz(i)
    ##     os.system('cp quizzes/practice%d/practice%d.pdf www/restricted' % (i,i))


def make_web(clean=True):

#     os.system("cp -r R/* www/R; rsync -avzh data/* www/data")
#     print "converting notebooks to rst"

#     table = [
#         ('Diamonds.ipynb', 'diamonds.rst'),
#         ('Unemployment Data.ipynb', 'unemployment.rst'),
#         ('Some tips on R.ipynb', 'helpR.rst'),
#         ('Voting Records.ipynb', 'voting.rst'),
#         ('Discretization.ipynb', 'discretization.rst'),
#         ('PCA of olympic decathlon data.ipynb', 'olympic.rst'),
#         ('Some time series examples.ipynb', 'timeseries.rst'),
#         ('Distances.ipynb', 'distances.rst'),
#         ('Simple visualization.ipynb', 'visualization.rst'),
#         ('Multidimensional scaling.ipynb', 'mds.rst'),
#         ('Multidimensional arrays.ipynb', 'arrays.rst'),
#         ('Trees.ipynb', 'trees.rst'),
#         ('Linear Discriminant Analysis.ipynb', 'lda.rst'),
#         ('Classifiers.ipynb', 'classifiers.rst'),
#         ('SVMS.ipynb', 'svms.rst'),
#         ('Ensemble methods.ipynb', 'ensemble.rst'),
#         ('Kmeans.ipynb', 'kmeans.rst'),
#         ('Hierarchical clustering.ipynb', 'hierarchical.rst'),
#         ('Model based clustering.ipynb', 'model_cluster.rst'),
#         ('LASSO.ipynb', 'lasso.rst')]

#     batch('notebooks', 'web', table)
#     os.system('mkdir www/notebooks; cp notebooks/*ipynb www/notebooks')

    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    
    for nbook in glob.glob('notebooks/*ipynb'):
        os.system('nbconvert.py --preamble=latex/header.tex -f latex "%s" ' % nbook)
        texfile = (os.path.splitext(nbook)[0] + '.tex')
        shutil.copy(texfile, 'notebooks/tmp.tex')
        os.system(r'cd notebooks; pdflatex "\nonstopmode\input{tmp.tex}"; mv tmp.pdf "%s"' % (os.path.basename(texfile)[:-3] + 'pdf'))

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
