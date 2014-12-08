#!/bin/bash


##############################################################################
# This script builds the bottle documentation for a specific git branch.
##############################################################################

cd $(dirname $0)
set -e

if [ $# -ne 2 ]; then
  echo "Usage: $0 branch output_folder"
  echo "Example: $0 master docs/dev"
  exit 0
fi

for cmd in git tar zip make rsync sphinx-build pdflatex makeindex; do
  hash $cmd 2>&- || {
    echo >&2 "Please install '$cmd' first. Aborting."
    exit 1
  }
done

repo_dir='/tmp/update_docs_bottle.git'
build_dir='/tmp/update_docs_bottle.build'
branch=$1
output=$2

test -d $repo_dir || git clone git://github.com/bottlepy/bottle.git $repo_dir
pushd $repo_dir
 git fetch origin
 git checkout -f "docs-$branch" || git checkout -f -b "docs-$branch" "origin/$branch"
 git clean -d -x -f
 git pull
 test -d apidocs && cd apidocs || cd docs
 docs=`pwd`
popd

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

