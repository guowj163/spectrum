#!/usr/bin/env python
# coding=utf-8



import os
import glob
import webbrowser
from astropy.io import fits as pyfits
from PyAstronomy import pyasl
import sys

def obj_lst(reboot):
        #读取目标的赤经赤纬
    scriptpath = os.path.dirname(os.path.abspath(__file__))
    lst = [i.split() for i in file(scriptpath+os.sep+'objradec.lst')]
    namelst = [i[0] for i in lst]
    ralst = [float(i[1]) for i in lst]
    declst = [float(i[2]) for i in lst]


    fitnamelst = glob.glob('ftb*.fits')
    namedic = {}
    # fitnamelst = [i for i in fitnamelst if
    #               pyfits.getval(i, 'INSFLNAM').strip().lower() == 'johnsonv']
    print'1'
        #进行Ra,Dec匹配
    for fitname in fitnamelst:

        ra = pyfits.getval(fitname, 'RA')
        dec = pyfits.getval(fitname, 'DEC')
        objname = pyfits.getval(fitname, 'OBJECT')
        flag = False

        for i, name in enumerate(namelst):
            angdis = pyasl.getAngDist(ralst[i], declst[i], ra, dec)
            
            if angdis < 0.6:
                flag = True
                print '%s  %15s  ---->  %s' % (fitname, objname, name)
                if name in namedic:
                    namedic[name].append(fitname)
                else:
                    namedic[name] = [fitname]
                break

        if flag is False:
            print '%s  %s  %f  %f  not found in objradec.lst' % (fitname, objname, ra, dec)
            print 'please check the fits file ,edit and save objradec.lst!!!'
            webbrowser.open(scriptpath+os.sep+'objradec.lst')
            if ra==0 and dec==0:
                os.remove(fitname)
                reboot=1
                break
            else:
                raw_input('press any key to reboot')
                reboot=1
                break
        
    
    if reboot == 0:
        #生成目标list文件
        for name in namedic:
            fn = 'obj_'+name+'.lst'
            fil = open(fn, 'w')
            for fitname in namedic[name]:
                fil.write(fitname+'\n')
            fil.close()
    return reboot


def main():
    """
    creat object lst.
    through match radec file 'objradec.lst'
    """

    print '='*50
    print '<<<<<run  generate_objlst.py  >>>>>'   
                #删除目标list文件
    objfile=glob.glob('obj*.lst')
    for i in objfile:
        os.remove(i)
    print '<<<<<clear all the object list >>>>>'

    mark=0
    mark=obj_lst(mark)

    while mark==1:
        print'!!!!!rerun  generate_objlst.py !!!!!'
        mark=0
        mark=obj_lst(mark)
    print('<<<<< run generate_objlst.py successfully >>>>>  ')
    print '='*50



if __name__ == '__main__':
    main()