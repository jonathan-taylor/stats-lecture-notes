import os, glob, shutil, filecmp
from stats_lectures.nbtools import strip_skipped_cells, reads, writes

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.dirname(nbook))
    shutil.copy2('stats60_article.tplx', nbook_dir)
    shutil.copy2('stats60_slides.tplx', nbook_dir)
    shutil.copy2('stats60_html.tplx', nbook_dir)
    cmd = '''
    cd "%s"; 
    ipython nbconvert --to=slides "%s" --template=./stats60_slides.tplx;
    ipython nbconvert --to=html "%s" --template=./stats60_html.tplx;
    ''' % (nbook_dir, 
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
    cp -r ../../notebooks/stats60/index.ipynb .;
    ipython nbconvert --to rst index.ipynb; rm index.ipynb ;
    ''')

    for obook in glob.glob('../../notebooks/stats60/Week*/*ipynb'):
        nbook = obook.replace('../../', './').replace('stats60/', '')
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
            stripped_nb = strip_skipped_cells(nb)
            with open(nbook.replace('.ipynb', '_stripped.ipynb'), 'w') as f:
                f.write(writes(nb, 'json'))
            build_nbook(nbook.replace('.ipynb', '_stripped.ipynb'))

    for week in glob.glob('notebooks/Week*'):
        wwwdir = week.replace('notebooks', 'www')
        if not os.path.exists(wwwdir):
            shutil.copytree(week, wwwdir)
        else:
            for f in glob.glob('%s/*' % week):
                shutil.copy2(f, wwwdir)

    for f in glob.glob('www/Week*/*stripped.*'):
        os.rename(f, f.replace('_stripped', ''))

    cmd = '''
    make html; 
    cp -r _build/html/* www; 
    '''
    os.system(cmd)


def deploy():
    os.system("""
    rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats60/WWW/ ;
    rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats60/www ;
    """)

