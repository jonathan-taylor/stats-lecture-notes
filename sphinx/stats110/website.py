import os, glob, shutil, filecmp
from stats_lectures.nbtools import strip_skipped_cells, reads, writes

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.dirname(nbook))
    shutil.copy2('stats110_article.tplx', nbook_dir)
    shutil.copy2('stats110_slides.tplx', nbook_dir)
    shutil.copy2('stats110_html.tplx', nbook_dir)
    cmd = '''
    cd "%s"; 
    ipython nbconvert --to=slides "%s" --template=./stats110_slides.tplx --reveal-prefix=http://stats110.stanford.edu/reveal.js;
    ipython nbconvert --to=latex --post=pdf "%s" --template=./stats110_article.tplx;
    ipython nbconvert --to=html "%s" --template=./stats110_html.tplx;
    ''' % (nbook_dir, 
            os.path.abspath(nbook),
            os.path.abspath(nbook),
            os.path.abspath(nbook))
    print cmd
    os.system(cmd)

def make_web(clean=True, force=False):

    if clean:
        os.system('make clean;')
    
    for dir in ['www', 'notebooks']:
        if not os.path.exists(dir):
            os.makedirs(dir)
    os.system('''
    cp -r ../../notebooks/stats110/index.ipynb .;
    ipython nbconvert --to rst index.ipynb; rm index.ipynb ;
    cp -r ../../notebooks/stats110/Topics\ for\ review.ipynb .;
    ipython nbconvert --to rst Topics\ for\ review.ipynb; rm Topics\ for\ review.ipynb ;
    ''')

    for obook in (glob.glob('../../notebooks/stats110/Week*/*ipynb') + 
                  glob.glob('../../notebooks/stats110/Examples/*ipynb')):
        nbook = obook.replace('../../', './').replace('stats110/', '')
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

    for dirname in glob.glob('built_notebooks/Week*') + ['built_notebooks/Examples']:
        wwwdir = dirname.replace('built_notebooks', 'www')
        if not os.path.exists(wwwdir):
            shutil.copytree(dirname, wwwdir)
        else:
            for f in glob.glob('%s/*' % dirname):
                if not os.path.isdir(f):
                    shutil.copy2(f, wwwdir)

    for f in (glob.glob('www/Week*/*stripped.*') + 
              glob.glob('www/Examples/*stripped.*')):
        os.rename(f, f.replace('_stripped', ''))

    cmd = '''
    make html; 
    rm -fr _build/html/quizzes;
    rm -fr _build/html/_sources;
    cp -r _build/html/* www; 
    cp -r edited_notes/ www/edited_notes;
    '''
    os.system(cmd)


def deploy():
    os.system('''
    rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats110/WWW/ ;
    # ssh jtaylo@corn.stanford.edu "cd stats-lecture-notes; git fetch ; git pull";
    # rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats110/www ;
    ''')

