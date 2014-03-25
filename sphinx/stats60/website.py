import os, glob, shutil, filecmp

def build_nbook(nbook):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    shutil.copy2('stats60_article.tplx', nbook_dir)
    shutil.copy2('stats60_slides.tplx', nbook_dir)
    cmd = '''
    cd %s; 
    ipython nbconvert --to=slides "%s" --template=./stats60_slides.tplx;
    ipython nbconvert --to=html "%s";
    ''' % (nbook_dir, 
            os.path.abspath(nbook),
            os.path.abspath(nbook))
    cmd += '''
ipython nbconvert --to=latex --post PDF --template=stats60_article.tplx "%s";
''' % os.path.abspath(nbook)
    os.system(cmd)

def make_web(clean=True, force=False):

    if clean:
        os.system('make clean;')
    
    os.system('mkdir -p notebooks; cp -r ../../notebooks/stats60/index.ipynb .')        
    os.system('ipython nbconvert --to rst index.ipynb; rm index.ipynb')
    os.system('mkdir -p notebooks; cp -r ../../notebooks/stats60/* notebooks/')        
    os.system('mkdir -p www/R; cp R/* www/R; cp -r assignments/* notebooks/; rm -fr notebooks/oldslides notebooks/oldnotebooks')        
    os.system('cp -r assignments/* notebooks/; rm -fr notebooks/oldslides notebooks/oldnotebooks')        

    for nbook in glob.glob('notebooks/*ipynb'):
        htmlfile = os.path.splitext(nbook)[0] + '.html'
        pdffile = os.path.splitext(nbook)[0] + '.pdf'
        try:
            diff_file = not (filecmp.cmp(htmlfile, 
                                         os.path.join('www', htmlfile))
                             and filecmp.cmp(pdffile, 
                                             os.path.join('www', pdffile)))
        except OSError:
            diff_file = True
            
        if force or diff_file:
            build_nbook(nbook)

    os.system('mkdir -p  www/notebooks/figs ; cp latex/header.tex www;')
    os.system("mkdir -p www/data; cp ../../data/* www/data; cp -r notebooks/* www/notebooks; make html; cp -r _build/html/* www; ")

def deploy():
    os.system('rm -fr www/notebooks/oldnotebooks www/notebooks/oldslides ')
    os.system("rsync -avz www/* jtaylo@corn.stanford.edu:/afs/ir/class/stats60/WWW/")
    os.system("rsync -avz www/* jtaylo@miller.stanford.edu:stats-lecture-notes-working/sphinx/stats60/www")

