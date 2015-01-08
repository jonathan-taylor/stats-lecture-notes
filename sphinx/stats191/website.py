import os, glob, shutil, filecmp
from stats_lectures.nbtools import strip_skipped_cells, reads, writes

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats191_article.tplx', nbook_dir)
    shutil.copy2('stats191_slides.tplx', nbook_dir)
    cmd = '''
    cd "%s"; 
    ipython nbconvert --to=slides "%s" --template=./stats191_slides.tplx --reveal-prefix=http://statweb.stanford.edu/~jtaylo/reveal.js;
    ipython nbconvert --to=html "%s";
    ''' % (nbook_dir, 
            os.path.abspath(nbook),
            os.path.abspath(nbook))
    cmd += '''
ipython nbconvert --to=latex --post PDF --template=stats191_article.tplx "%s";
''' % os.path.abspath(nbook)
    os.system(cmd)

def make_web(clean=True, force=False, assigned=[1], solved=[]):

    if clean:
        os.system('make clean;')
    
    for dir in ['www', 'notebooks']:
        if not os.path.exists(dir):
            os.makedirs(dir)

    for obook in glob.glob('../../notebooks/stats191/*ipynb'):
        nbook = obook.replace('../../', './').replace('stats191/', '')
        print nbook
        if not os.path.exists(os.path.dirname(nbook)):
            os.makedirs(os.path.dirname(nbook))
        try:
            diff = not filecmp.cmp(obook, nbook)
        except OSError:
            diff = True

        if diff:
            shutil.copy(obook, nbook) 
            with open(nbook, 'r') as f:
                nb = reads(f.read(), 'json')
            print 'running and stripping skipped cells from notebook %s' % nbook
            stripped_nb = strip_skipped_cells(nb, timeout=10)

            new_nbook = nbook.replace('notebooks', 'built_notebooks')
            if not os.path.exists(os.path.dirname(new_nbook)):
                os.makedirs(os.path.dirname(new_nbook))
            with open(new_nbook, 'w') as f:
                f.write(writes(nb, 'json'))
            build_nbook(new_nbook)

    for dirname in ['built_notebooks']:
        wwwdir = dirname.replace('built_notebooks', 'www/notebooks')
        if not os.path.exists(wwwdir):
            shutil.copytree(dirname, wwwdir)
        else:
            for f in glob.glob('%s/*' % dirname):
                if not os.path.isdir(f):
                    shutil.copy2(f, wwwdir)

    for f in (glob.glob('www/notebooks/*stripped.*') + 
              glob.glob('www/notebooks/*stripped.*')):
        os.rename(f, f.replace('_stripped', ''))

    del_assign = set(range(1,6)).difference(assigned)
    for assign in del_assign:
        for f in glob.glob('www/notebooks/Assignment%d*' % assign):
            os.remove(f)

    del_solved = set(range(1,6)).difference(solved)
    for solve in del_solved:
        for f in glob.glob('www/notebooks/Solution%d*' % solve):
            os.remove(f)

    cmd = '''
    make html; 
    rm -fr _build/html/quizzes;
    rm -fr _build/html/_sources;
    cp -r _build/html/* www; 
    '''
    os.system(cmd)


def deploy():
    os.system('rm -fr www/notebooks/oldnotebooks www/notebooks/oldslides ')
    os.system("rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats191/WWW/")
#    os.system("rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats191/www")

