#!/usr/bin/env bash

# set -e

baseDirForScriptSelf=$(cd "$(dirname "$0")"; pwd)

# if  [ -d photo ]; then
#    cd photo
#    rm caf*.fits 2>/dev/null
# fi
cd `pwd`

python ${baseDirForScriptSelf}/mvto_photo.py

cd photo

   python ${baseDirForScriptSelf}/generate_lst.py
   python ${baseDirForScriptSelf}/reduce_img.py
   python ${baseDirForScriptSelf}/generate_objlst.py

cd ..