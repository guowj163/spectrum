#! /bin/bash


baseDirForScriptSelf=$(cd "$(dirname "$0")"; pwd)

${baseDirForScriptSelf}/run_ds9_or_ximtool.sh

${baseDirForScriptSelf}/cp_to_spec.py

cd spec

    ${baseDirForScriptSelf}/list_and_check.py
    ${baseDirForScriptSelf}/cor_ftbo.py
    ${baseDirForScriptSelf}/lampcomb_wavelenthcalib.py
    ${baseDirForScriptSelf}/re_apall.py
    ${baseDirForScriptSelf}/re_corflux.py
cd ..




