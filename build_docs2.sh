#!/bin/bash


##############################################################################
# This script builds the bottle documentation for a specific git branch.
##############################################################################

cd $(dirname $0)
set -e

for cmd in git tar zip make rsync sphinx-build pdflatex makeindex; do
  hash $cmd 2>&- || {
    echo >&2 "Please install '$cmd' first. Aborting."
    exit 1
  }
done

repo_dir='/tmp/update_docs_bottle.git'
build_dir='/tmp/update_docs_bottle.build'

build() {
  branch=$1
  output=$2
  lang=$3

  test -d $repo_dir || git clone git://github.com/bottlepy/bottle.git $repo_dir
  pushd $repo_dir
   git fetch origin
   git checkout -f -B "docs-$branch" "origin/$branch"
   git clean -d -x -f
   test -d apidocs && cd apidocs || cd docs
   docs=`pwd`
   test -d $docs/_locale && bash $docs/_locale/update.sh
  popd

  sphinx="sphinx-build -q -c sphinx -Dlanguage=$lang"
  PYTHONPATH=$repo_dir $sphinx -b html     $docs $build_dir/$branch/html
  PYTHONPATH=$repo_dir $sphinx -b latex    $docs $build_dir/$branch/latex
  PYTHONPATH=$repo_dir $sphinx -b bottlepy $docs $build_dir/$branch/pickle

  pushd $build_dir/$branch
   pushd latex
    pdflatex -halt-on-error Bottle.tex > latex.log &&\
    pdflatex -halt-on-error Bottle.tex >> latex.log &&\
    pdflatex -halt-on-error Bottle.tex >> latex.log &&\
    makeindex -s python.ist Bottle.idx >> latex.log &&\
    pdflatex -halt-on-error Bottle.tex >> latex.log &&\
    pdflatex -halt-on-error Bottle.tex >> latex.log
    test -e Bottle.pdf || cat latex.log
   popd
   cp latex/Bottle.pdf bottle-docs.pdf || true
   tar -czf bottle-docs.tar.gz html
   tar -cjf bottle-docs.tar.bz2 html
   zip -q -r -9 bottle-docs.zip html
   cp bottle-docs.* html
  popd

  # We rsync to keep mtime on unchanged files. Good for HTTP caching.
  test -d "$output/" || mkdir -p "$output/"
  rsync -vrc --exclude .doctrees $build_dir/$branch/html/ "$output/"
  rsync -vrc --exclude .doctrees $build_dir/$branch/pickle/ "$output/"
  rm -rf $build_dir/$branch
}

build "master" "/home/marc/bottlepy.org/docs/dev-cn" "zh_CN"


