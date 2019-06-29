#!/usr/bin/env bash

curpath=`pwd`
rootdir=`dirname ${curpath}`
baseDirForScriptSelf=$(cd "$(dirname "$0")"; pwd)

cd ${rootdir}
if ! [ -d object ]; then
  mkdir object
fi

if [ -d ${baseDirForScriptSelf}/step2 ];then
  cp -R ${baseDirForScriptSelf}/step2 ${objdir}
fi

objdir=${rootdir}/object

cd ${curpath}

read -p "if you want to clear all the data and reduce,pealse input 'clear' !" input_argument

if [ "$input_argument" == 'clear' ];then
  echo 'Waring!!! clear reduce all the data'
  
  for dirname in `ls *CAFOS -d`;do
    cd ${curpath}/${dirname}

    bash ${baseDirForScriptSelf}/phot_reduce.sh
    bash ${baseDirForScriptSelf}/copy_ftb_to_object.sh ${objdir}
  
    cd ..
  done


else
  check_update=`cat check_update.lst`
  
  for dirname in `ls *CAFOS -d`; do 
    result=$(echo $check_update | grep "${dirname}")
    if [[ "$result" == "" ]]
    then
      echo $dirname

      cd ${curpath}/${dirname}

      bash ${baseDirForScriptSelf}/phot_reduce.sh

      bash ${baseDirForScriptSelf}/copy_ftb_to_object.sh  ${objdir}
  
      cd ..
    fi
  done
fi

ls *CAFOS -d > check_update.lst
cp check_update.lst  `date "+%Y%m%d"`



