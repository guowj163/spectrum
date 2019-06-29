#!/usr/bin/env bash

# if  [ -d photo ]; then
#     cd ${curpath}/photo
# fi
cd photo
for lstname in `ls obj_*.lst`; do
    outdirname=${lstname%.*}
    
    outdir=${1}/${outdirname}
    if ! [ -d ${outdir} ]; then
        echo mkdir ${outdir}
        mkdir ${outdir}
    fi

    if ! [ -d ${outdir}/images ]; then
        echo mkdir ${outdir}/images
        mkdir ${outdir}/images
    fi
    imagepath=${outdir}/images

    for fname in `cat $lstname`; do

        if ! [ -f ${imagepath}/${fname} ]; then
        echo \<\<\<copy ${fname} ${imagepath}\>\>\>
        cp -v ${fname} ${imagepath}
        fi
    done

done