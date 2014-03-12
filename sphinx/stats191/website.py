import os, glob, shutil

def build_nbook(nbook, build_pdf=True):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats191_article.tplx', nbook_dir)
    shutil.copy2('slides_reveal2.tpl', nbook_dir)
    cmd = '''
cd %s; 
ipython nbconvert --to=slides "%s" --template=./stats191_slides.tplx;
ipython nbconvert --to=html "%s";
 ''' % (nbook_dir, 
        os.path.abspath(nbook),
        os.path.abspath(nbook))
    if build_pdf:
        cmd += '''
ipython nbconvert --to=latex --post PDF --template=stats191_article.tplx "%s";
''' % os.path.abspath(nbook)
    os.system(cmd)

def make_web(clean=True, build_pdf=True):

    if clean:
        os.system('make clean;')
    
    os.system('mkdir -p notebooks; cp -r ../../notebooks/stats191/* notebooks/')        
    os.system('mkdir -p www/R; cp R/* www/R; cp -r assignments/* notebooks/; rm -fr notebooks/oldslides notebooks/oldnotebooks')        
    os.system('cp -r assignments/* notebooks/; rm -fr notebooks/oldslides notebooks/oldnotebooks')        
    if build_pdf:
        for nbook in glob.glob('notebooks/*ipynb'):
            build_nbook(nbook, build_pdf=build_pdf)

    os.system('mkdir -p  www/notebooks/figs ; cp latex/header.tex www;')
    os.system("mkdir -p www/data; cp ../../data/* www/data; cp -r notebooks/* www/notebooks; make html; cp -r _build/html/* www; ")

def deploy():
    os.system('rm -fr www/notebooks/oldnotebooks www/notebooks/oldslides ')
    os.system("rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats191/WWW/")
    os.system("rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats191/www")

