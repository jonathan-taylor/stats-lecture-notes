import os, glob, shutil

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats191_article.tplx', nbook_dir)
    shutil.copy2('stats191_slides.tplx', nbook_dir)
    cmd = '''
cd %s; 
ipython nbconvert --to=latex --post PDF --template=stats191_article.tplx "%s";
ipython nbconvert --to=slides --template=stats191_slides.tplx "%s";
ipython nbconvert --to=html "%s";
 ''' % (nbook_dir, 
        os.path.abspath(nbook),
        os.path.abspath(nbook),
        os.path.abspath(nbook))
    os.system(cmd)

def make_web(clean=True, build_pdf=True):

    if clean:
        os.system('make clean;')
    
    if build_pdf:
        
        os.system('mkdir -p notebooks; cp -r ../../notebooks/stats191/* notebooks/')        
        for nbook in glob.glob('notebooks/*ipynb'):
            build_nbook(nbook)


    os.system('mkdir -p  www/notebooks/figs ; mkdir www/exercises ; cp latex/header.tex www;')
    os.system("mkdir www/data; cp data/* www/data; cp -r notebooks/* www/notebooks; make html; cp -r _build/html/* www; ")

def deploy():
    os.system("rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats191/WWW/")

