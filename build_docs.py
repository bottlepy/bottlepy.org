import sys, os
from subprocess import call, check_call
import argparse
import tempfile

parser = argparse.ArgumentParser(description='Build the documentation')
parser.add_argument('--git',
                   default='https://github.com/bottlepy/bottle.git',
                   help='Path or URL to git repository')
parser.add_argument('--config',
                   help='Path to the sphinx config file.')
parser.add_argument('--clonedir',
                   help='Path to the local git repository clone.')
parser.add_argument('--builddir',
                   help='Path to the local build directory.')
parser.add_argument('branch', 
                   help='GIT branch or tag to build')
parser.add_argument('output', 
                   help='Output directory')

def die(msg):
    sys.stderr.write(msg.strip()+'\n');
    sys.exit(1)

def check_required_commands():
    for cmd in 'git tar zip make rsync sphinx-build pdflatex makeindex'.split():
        if call(['hash', cmd]):
            die('Command not found: $r' % cmd)

def build():
    args = parser.parse_args()
    git_dir   = args.clonedir\
                or tempfile.mkdtemp(prefix='bottle-build-docs', suffix='.git')
    build_dir = args.builddir\
                or tempfile.mkdtemp(prefix='bottle-build-docs', suffix='.build')

    branch = args.branch
    output = args.output

    if not os.path.isdir(git_dir)\
    or not os.path.isdir(os.path.join(git_dir, '.git')):
        check_call(['git', 'clone', args.git, git_dir])
    check_call(['git', 'fetch', 'origin'], cwd=git_dir)
    check_call(['git', 'checkout', '-f',
                '-B', 'docs-%s' % branch,
                'origin/%s' % branch], cwd=git_dir)
    check_call(['git', 'clean', '-d', '-x', '-f'], cwd=git_dir)
    if os.path.isdir(os.path.join(git_dir, 'apidocs')):
        docs_dir = os.path.join(git_dir, 'apidocs')
    else:
        docs_dir = os.path.join(git_dir, 'docs')
    
    os.environ['PYTHONPATH'] = git_dir + os.sep + os.environ.get('PYTHONPATH','')
    
    for mode in ['html', 'latex', 'bottlepy']:
        cmd  = ['sphinx-build', '-q', '-c', 'sphinx']
        cmd += ['-b', mode]
        cmd += [docs_dir, os.path.join(build_dir, branch, mode)]
        check_call(cmd)

build()


'''

PYTHONPATH=$repo_dir sphinx-build -q -c sphinx -b html     $docs $build_dir/$branch/html
PYTHONPATH=$repo_dir sphinx-build -q -c sphinx -b latex    $docs $build_dir/$branch/latex
PYTHONPATH=$repo_dir sphinx-build -q -c sphinx -b bottlepy $docs $build_dir/$branch/pickle

pushd $build_dir/$branch
 pushd latex
  pdflatex -halt-on-error Bottle.tex > latex.log
  pdflatex -halt-on-error Bottle.tex >> latex.log
  pdflatex -halt-on-error Bottle.tex >> latex.log
  makeindex -s python.ist Bottle.idx >> latex.log
  pdflatex -halt-on-error Bottle.tex >> latex.log
  pdflatex -halt-on-error Bottle.tex >> latex.log
  test -e Bottle.pdf || exit 1
 popd
 cp latex/Bottle.pdf bottle-docs.pdf
 tar -czf bottle-docs.tar.gz html
 tar -cjf bottle-docs.tar.bz2 html
 zip -q -r -9 bottle-docs.zip html
 cp bottle-docs.* html
 cp $repo_dir/bottle.py html
popd

# We rsync to keep mtime on unchanged files. Good for HTTP caching.
test -d "$output/" || mkdir -p "$output/"
rsync -vrc --exclude .doctrees $build_dir/$branch/html/ "$output/"
rsync -vrc --exclude .doctrees $build_dir/$branch/pickle/ "$output/"
rm -rf $build_dir/$branch
'''

