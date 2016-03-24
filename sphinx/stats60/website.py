import os, glob, shutil, filecmp
import sys

# from https://github.com/cfriedline/ipynb_template

from nbformat import v4

def strip_output(nb, delete_if = lambda cell: False):
    """strip the outputs from a notebook object"""
    for cell in nb.cells:
        if 'slideshow' in cell['metadata'] and cell['metadata']['slideshow']['slide_type'] == 'skip':
            nb.cells.remove(cell)
        if 'outputs' in cell:
            cell['outputs'] = []
        if 'execution_count' in cell:
            cell['execution_count'] = 0
    return nb

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats60_article.tplx', nbook_dir)
    shutil.copy2('stats60_slides.tplx', nbook_dir)
    cmd = '''
    cd "%s"; 
    jupyter-nbconvert --to=slides "%s" --template=./stats60_slides.tplx --reveal-prefix=http://statweb.stanford.edu/~jtaylo/reveal.js;
    jupyter-nbconvert --to=html "%s";
    jupyter-nbconvert --to=rst "%s";
    ''' % (nbook_dir, 
            os.path.abspath(nbook),
            os.path.abspath(nbook),
            os.path.abspath(nbook))
    cmd += '''
jupyter-nbconvert --to=latex --template=stats60_article.tplx "%s";
''' % os.path.abspath(nbook)
    os.system(cmd)

def make_web(clean=True, force=False, assigned=[1,2,3,4], solved=[1,2,3]):

    if clean:
        os.system('make clean;')
    
    for dir in ['www', 'notebooks']:
        if not os.path.exists(dir):
            os.makedirs(dir)

    for obook in glob.glob('../../notebooks/stats60/*ipynb'):
        nbook = obook.replace('../../', './').replace('stats60/', '')
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
                nb = v4.reads(f.read())
            #print 'stripping output from notebook %s' % nbook
            stripped_nb = nb # strip_output(nb)
            new_nbook = nbook.replace('notebooks', 'built_notebooks')
            if not os.path.exists(os.path.dirname(new_nbook)):
                os.makedirs(os.path.dirname(new_nbook))
            with open(new_nbook, 'w') as f:
                f.write(v4.writes(nb).encode('utf-8'))
            build_nbook(new_nbook)

    for dirname in ['built_notebooks']:
        wwwdir = dirname.replace('built_notebooks', 'www/notebooks')
        if not os.path.exists(wwwdir):
            shutil.copytree(dirname, wwwdir)
        else:
            for f in glob.glob('%s/*' % dirname):
                if not os.path.isdir(f):
                    shutil.copy2(f, wwwdir)

    shutil.copy('built_notebooks/index.rst', 'index.rst')

#     for f in (glob.glob('www/notebooks/*stripped.*') + 
#               glob.glob('www/notebooks/*stripped.*')):
#         os.rename(f, f.replace('_stripped', ''))

#     del_assign = set(range(1,6)).difference(assigned)
#     for assign in del_assign:
#         for f in glob.glob('www/notebooks/Assignment%d*' % assign):
#             os.remove(f)

#     del_solved = set(range(1,6)).difference(solved)
#     for solve in del_solved:
#         for f in glob.glob('www/notebooks/Solution%d*' % solve):
#             os.remove(f)

    cmd = '''
    make html; 
    rm -fr _build/html/_sources;
    cp -r _build/html/* www; 
    mkdir -p www/R;
    cp -r R/* www/R;
    '''
    os.system(cmd)


def deploy():
    #os.system("cp data/* www/data; rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats60/WWW/")
    os.system("cp data/* www/data; rsync -avz www/* jtaylo@rgmiller:public_html/stats60/")


