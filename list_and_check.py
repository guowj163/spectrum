#!/usr/bin/env python
# -*- encoding=utf-8 -*-

"""
Generate lst file for different fits type.
the lst file include :
    spec_bias.lst
    all.lst
    halogen.lst
    cor_halogen.lst
    lamp.lst
    cor_lamp.lst
    std.lst
    cor_std.lst
"""

import os
import glob
import numpy as np
from astropy.io import fits as pyfits
import webbrowser
from pyraf import iraf



script_path = os.path.dirname(os.path.realpath(__file__))
config_path = script_path + os.sep + 'config'

def is_std(fn):

    stdlstname = config_path + os.sep + 'standard.lst'
    stdlst = open(stdlstname).readlines()
    stdset = set([i.split()[0].lower() for i in stdlst])

    objname = pyfits.getval(fn, 'OBJECT').split()[0].lower()
    if objname in stdset:
        return True
    for name in stdset:
        if name in objname:
            return True
    return False

def is_halogen(fn):

    val = pyfits.getval(fn, 'IMAGETYP').strip().lower()
    return val == 'flat'

def is_lamp(fn):

    val2 = pyfits.getval(fn, 'HIERARCH CAHA INS LAMP1 STATUS').lower()
    val3 = pyfits.getval(fn, 'HIERARCH CAHA INS LAMP2 STATUS').lower()
    val4 = pyfits.getval(fn, 'HIERARCH CAHA INS LAMP3 STATUS').lower()
    if val2 == 'on' or val3 == 'on' or val4 == 'on':
        return True
    else:
        return False


def is_bias(fn):
    val = pyfits.getval(fn, 'EXPTIME')
    if val == 0.0:
        return True
    else:
        return False

def write_to_file(namelst, outname):
    fil = open(outname, 'w')
    for name in namelst:
        text = name.strip()
        val = pyfits.getval(name, 'OBJECT')
        print('%s  %-33s  ---->  %s' % (text, val, outname))
        fil.write(text+'\n')
    fil.close()


def check():
    lstlst = ['spec_bias.lst', 'halogen.lst', 'lamp.lst', 
              'std.lst', 'cor_std.lst']
    for i in lstlst:
        if os.path.isfile(i):
            webbrowser.open(i)
            iraf.imexamine(input='@%s' % i, frame=1)
            if 'i'=='cor_std.lst':
                break

def main():
    namelst = np.array(sorted(glob.glob('caf*.fits')))

    argbias = np.array([is_bias(name) for name in namelst])

    argall = argbias == False
    arghalogen = np.array([is_halogen(name) for name in namelst])

    argcor_halogen = argall & (arghalogen == False)
    
    arglamp = np.array([is_lamp(name) for name in namelst])
    argcor_lamp = argcor_halogen & (arglamp == False)

    exptime = np.array([pyfits.getval(name, 'EXPTIME') for name in namelst])
    argexptimelg30 = exptime >= 20
    argcor_lamp = argcor_lamp & argexptimelg30

    argstd = np.array([is_std(name) for name in namelst]) & argcor_lamp
    argobj = argcor_lamp & (argstd == False)
    write_to_file(namelst[argbias], 'spec_bias.lst')
    write_to_file(namelst[argall], 'all.lst')
    write_to_file(namelst[arghalogen], 'halogen.lst')
    write_to_file(namelst[argcor_halogen], 'cor_halogen.lst')
    
    write_to_file(namelst[argcor_lamp], 'cor_lamp.lst')
    write_to_file(namelst[argstd], 'std.lst')
    write_to_file(namelst[argobj], 'cor_std.lst')
    
        #select the slit of 3 arc
    lamplst=namelst[arglamp]
    cahalamp=[]
    for name in lamplst:
        slit_lenth=pyfits.getval(name, 'HIERARCH CAHA INS SLIT WID')
        if slit_lenth > 150:
            cahalamp.append(name)

    write_to_file(cahalamp, 'lamp.lst')
    check()

if __name__ == '__main__':
    main()





