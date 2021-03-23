#!/bin/bash

git submodule init
git submodule update
git submodule foreach git config credential.helper store
git submodule foreach git checkout -B master origin/master

echo "Change into tools-multisetup"
cd tools-multisetup/
git submodule init
git submodule update
