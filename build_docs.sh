#!/bin/bash

cd $(dirname $0)
set -e
set -x

branch=$1
output=$2
venv_dir="./build/venv"
repo_dir="./build/bottle.git"
build_dir="./build/docs/"

mkdir -p "$build_dir"
test -d "$venv_dir" || python3 -mvenv "$venv_dir"
source "$venv_dir/bin/activate"
pip install -r requirements.txt
test -d $repo_dir || git clone https://github.com/bottlepy/bottle.git $repo_dir

pushd "$repo_dir"
  git fetch origin
  git switch --detach --force "origin/$branch"
  git clean -d -x -f
  test -d apidocs && cd apidocs || cd docs
  docs_dir=`pwd`
popd

rm -rf $build_dir/$branch/html/*
mkdir -p $build_dir/$branch/html

if [ "$output" == "--watch" ]; then
  PYTHONPATH=$repo_dir sphinx-autobuild -E -c sphinx -b html $docs_dir $build_dir/$branch/html
else
  PYTHONPATH=$repo_dir sphinx-build -E -q -c sphinx -b html $docs_dir $build_dir/$branch/html
  cp $repo_dir/bottle.py $build_dir/$branch/html

  # We rsync to keep mtime on unchanged files. Good for HTTP caching.
  mkdir -p "$output"
  rsync -vrc --exclude .doctrees --delete $build_dir/$branch/html/ "$output"
fi

