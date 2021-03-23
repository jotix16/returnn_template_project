#!/bin/bash

git submodule init
git submodule update
git submodule foreach git config credential.helper store
git submodule foreach git checkout -B master origin/master

echo "Change into tools-multisetup"
cd tools-multisetup/
git submodule init
git submodule update
cd ..


echo "Back to base_diri. Setup the symlinks."
dir_symlink="setup-data-dir-symlink"
if test "$dir_symlink"; then
  python setup-data-dir.py
  git commit $dir_symlink -m $dir_symlink
fi

newbob="newbob.data"
if test "$newbob"; then
  rm $newbob
fi

