import os, tempfile, glob, datetime, shutil

import scripts.strip_exercises as SE
reload(SE)
extract_exercises = SE.extract_exercises

templates = {'stats306b':'templates/stats306b_article.tplx',
             'stats191':'templates/stats191_article.tplx',
             }

def build_nbook(nbook, 
                course='stats306b'):
    nbook_dir = os.path.abspath(os.path.split(nbook)[0])
    tmp_dir = tempfile.mkdtemp()
    shutil.copy2(templates[course], tmp_dir)
    cmd = '''
cd %s; 
ipython nbconvert --to=latex --post PDF --template %s "%s"; 
cp *.pdf %s ''' % (tmp_dir, 
                   os.path.split(templates[course])[1],
                   os.path.abspath(nbook), 
                   nbook_dir)
    os.system(cmd)

def make_web(clean=True, build_pdf=True):

    if clean:
        cmd = 'make clean;'
    else:
        cmd = ''
    
    if build_pdf:
        
        for nbook in glob.glob('notebooks/stats306b/*ipynb'):
            build_nbook(nbook)
            extract_exercises([nbook], odir='exercises/stats306b')
            ebook = nbook.replace('notebooks', 'exercises')
            build_nbook(ebook)

    os.system('mkdir -p  www/restricted/notebooks ; mkdir www/exercises ; cp latex/header.tex www;')
    os.system("mkdir www/data; cp data/* www/data; cp exercises/*pdf www/exercises; cp notebooks/*ipynb notebooks/*pdf www/restricted/notebooks ; cd web; %s;  make html; cp -r _build/html/* ../www; ")

def deploy():
    os.system("rsync -avz www/* jtaylo@cardinal.stanford.edu:/afs/ir/class/stats306b/WWW")

