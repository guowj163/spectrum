#!/usr/bin/env python
# coding=utf-8 

import os
import glob
from astropy.io import fits as pyfits
import numpy as np
from pyraf import iraf
import sys

    #将list文件进行保存
def save_lst(list_name,contents):
    f=open(list_name,'w')
    contents.sort()
    for content in contents:
        f.write(content+'\n')
    f.close()

    
     #检查删除旧的list文件
def del_lst():
    oldlists=['all.lst','zero.lst','cor_zero.lst','flat.lst','cor_flat.lst']
    for oldlst in oldlists:
        if  os.path.isfile(oldlst):
            print 'remove the old list'
            os.remove(oldlst)

def main():
    """
    lst include:
        all.lst
        zero.lst
        cor_zero.lst
        flat.lst
        domeflat.lst
        cor_flat.lst
    the flat mean counts < 4000 and counts > 10000
    please be sure NAXIS1 and NAXIS2 in same size.
    """

    print('='*50)
    print('<<<<<run  generate_lst.py  # generate the list >>>>>')

    del_lst()
    
    namelst = glob.glob('caf*.fits')
    save_lst('all.lst',namelst)
    #print namelst

        #统计所有fits文件，以NAXIS众数为判断依据，检查fits文件是否有误
    widthlst = []
    hightlst = []
    for name in namelst:
        width = pyfits.getval(name, 'NAXIS1')
        hight = pyfits.getval(name, 'NAXIS2')
        widthlst.append(width)
        hightlst.append(hight)
    counts = np.bincount(widthlst)  
    width=np.argmax(counts)  
    counts = np.bincount(hightlst)  
    hight=np.argmax(counts)
    trimlst=[width,hight]
    print(trimlst)
    np.savetxt('trimlst',trimlst)
    

    namelst = [i for i in namelst if pyfits.getval(i, 'NAXIS1') == width and
               pyfits.getval(i, 'NAXIS2') == hight]
    zerolst = []
    flatlst = []
    objlst = []
    domeflatlst = []
        #生成各种list文件
    for name in namelst:
        mtype = pyfits.getval(name, 'IMAGETYP').lower()
        objname = pyfits.getval(name, 'OBJECT').lower()
        if mtype == 'flat' or 'sky'in objname or 'dome' in objname:
            fit = pyfits.open(name)
            med = np.median(fit[0].data)
            if med > 10000 and med < 45000:
                if 'dome'  in objname:
                    print ( name,' **domeflat.lst<-----',objname )
                    domeflatlst.append(name)
                else:
                    print ( name,' **flat.lst<-----',objname )
                    flatlst.append(name)
            else:
                if 'flat' not in objname:
                    print ( name,' ****cor_flat.lst<-----',objname )
                    objlst.append(name)
                    iraf.hedit(images=name, fields='IMAGETYP', value='science', add='No', addonly='No',
                    delete='no', verify='No', show='yes', update='Yes')


        elif mtype == 'bias' or 'bias' in objname:
            print ( name,' *zero.lst\t<-----',objname)
            zerolst.append(name)
        else:
            print ( name,' ****cor_flat.lst<-----',objname )
            objlst.append(name)

        #保存文件
    save_lst('zero.lst',zerolst)
        #默认采取sky flat作为平场，如果没有sky则采用dome flat
    if len(flatlst) == 0:
        print('Notice:fetch the dome sky flat as correct_flat file')
        flatlst = domeflatlst
        #domeflatlst = None
    save_lst('flat.lst',flatlst)
    cor_zerolst = flatlst + objlst
    if domeflatlst is not None:    
        cor_zerolst = cor_zerolst + domeflatlst  
        save_lst('domeflat.lst',domeflatlst)
    save_lst('cor_zero.lst',cor_zerolst)
    save_lst('cor_flat.lst',objlst)

    print('<<<<< run generate_lst.py successfully >>>>>  ')
    print('='*50)

if __name__ == '__main__':

    main()
