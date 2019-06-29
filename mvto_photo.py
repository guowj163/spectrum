#!/usr/bin/env python3
# coding=utf-8


import os
import glob
import shutil
from astropy.io import fits as pyfits
import numpy as np
import sys


def main():
    """
    mv photometric fits(pf) to dir photo,
    and mv the file size is same with pf to photo.
    pf is determined by keyword INSFLNAM == JohnsonV
    because the size of photometric fits is chaotic, I do not know how to get
    a better and easy way to do the same thing.
    assume pf have same size in same day, and all pf are observed with filter
    JohnsonV.
    """
    print('='*50)
    print('<<<run   mv_photo.py  # copy file to photo >>>')
    
    photoname='photo'
    namelst=glob.glob('caf*.fits')
  
        #检查fits文件名中是否含有‘：’，pyfits无法处理含：的fits文件
    error_namelst =[i for i in namelst if  ':' in i]
        #改正含有：的fits文件
    for errorname in error_namelst:
        new_name=errorname.replace(':','_')
        if not os.path.isfile(new_name):
            #print 'cp %s  %s' % (name, nname)
            print('copy',errorname,'\nto',new_name)
            shutil.move(errorname,new_name)
    
        #建立photo的目录
    if not os.path.isdir(photoname):
        print ('#  make a directory #', photoname)
        os.mkdir(photoname)

    namelst = glob.glob('caf*.fits')
    namelst = [i for i in namelst if ':' not in i and 'test' not in i]
        
        #将测光所需要的文件复制到photo目录下
        #条件： bias文件 含JohnsonV滤光片且不含狭缝即free的文件 排除test文件
    for name in namelst:
        val = pyfits.getval(name, 'INSAPID').lower()
        obj = pyfits.getval(name, 'OBJECT').lower()
        imtype = pyfits.getval(name, 'IMAGETYP').lower()
        insf= pyfits.getval(name, 'INSFLNAM')
        if imtype == 'bias' or 'bias' in obj.lower() or \
            (val == 'free' and insf == 'JohnsonV'and 'test'  not in obj.lower() and 'acq'  not in obj.lower()):
            print ('copy',name,'to',photoname)
            shutil.copy(name, photoname+os.sep+name)
    
    print('<<<run mv_photo.py successfully >>> ')
    print('='*50)

if __name__ == '__main__':

    main()

