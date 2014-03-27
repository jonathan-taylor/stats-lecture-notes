import os, glob, shutil, filecmp
from stats_lectures.nbtools import strip_skipped_cells, reads, writes

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats60_article.tplx', nbook_dir)
    shutil.copy2('stats60_slides.tplx', nbook_dir)
    shutil.copy2('stats60_html.tplx', nbook_dir)
    cmd = '''
    cd %s; 
    ipython nbconvert --to=slides "%s" --template=./stats60_slides.tplx;
    ipython nbconvert --to=html "%s" --template=./stats60_html.tplx;
    ipython nbconvert --to=latex --post PDF --template=stats60_article.tplx "%s";
    ''' % (nbook_dir, 
            os.path.abspath(nbook),
            os.path.abspath(nbook),
            os.path.abspath(nbook))
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

    for obook in glob.glob('../../notebooks/stats60/*ipynb'):
        nbook = obook.replace('../../', './').replace('stats60/', '')
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

    os.system('''
    cp -r notebooks/*stripped* www/notebooks; 
    make html; 
    cp -r _build/html/* www; 
    ''')

    for f in glob.glob('www/notebooks/*stripped.*'):
        os.rename(f, f.replace('_stripped', ''))
    for f in glob.glob('notebooks/*ipynb'):
        shutil.copy(f, 'www/' + f)

def deploy():
    os.system("""
    rm -fr www/notebooks/oldnotebooks www/notebooks/oldslides ;
    rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats60/WWW/ ;)
    rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats60/www ;
    """)

