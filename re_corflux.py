#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 22:08:34 2015

@author: zzx
"""

import os
from astropy.io import fits as pyfits
from pyraf import iraf
import numpy as np
import webbrowser

script_path = os.path.dirname(os.path.realpath(__file__)) 
config_path = script_path + os.sep + 'config' 
std_path = script_path+os.sep+'standarddir'  
stdpath = std_path+os.sep
extpath = config_path+os.sep+'kpnoextinct.dat'


    ######
def set_airmass(fn):

    fit = pyfits.open(fn)
    size = len(fit)
    for i, hdu in enumerate(fit):
        if 'AIRMASS' in hdu.header:
            airmassold = hdu.header['AIRMASS']
            print('%s[%d] airmassold = %f' % (fn, i, airmassold),)
            if 'AIROLD' in hdu.header:
                airold = hdu.header['AIROLD']
                print('%s[%d] AIROLD = %f' % (fn, i, airold))
                print('AIROLD keyword alreay exist, the airmass old will not saved')
            else:
                iraf.hedit(images=fn + '[%d]' % i, fields='AIROLD',
                           value=airmassold, add='Yes', addonly='Yes',
                           delete='No', verify='No', show='Yes', update='Yes')
    fit.close()
    ra, dec = get_ra_dec(fn)
    set_ra_dec(fn, ra, dec)

    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='ca',
                  caldir=stdpath)
    
    for i in range(size):
        iraf.setairmass(images=fn, observatory='ca',
                        intype='beginning', outtype='effective', ra='ra',
                        dec='dec', equinox='epoch', st='lst', ut='date-obs',
                        date='date-obs', exposure='exptime', airmass='airmass',
                        utmiddle='utmiddle', scale=750.0, show='yes',
                        override='yes', update='yes')

def get_ra_dec(fn):
    """
    get the source coords
    return : ra, dec (format like '12:34:56.78', '+23:45:67.89')
    """
    standname ,others = pyfits.getval(fn, 'OBJECT').split()   
    standname = standname.lower()
    radeclst = open(config_path + os.sep + 'objradec.lst').readlines()
    radecdic = dict([i.split(None, 1) for i in radeclst])
    if standname in radecdic:
        ra, dec = radecdic[standname].split()
        return ra, dec
    print('can not match ',standname ,', please check and edit objradec.lst')
    webbrowser.open(config_path + os.sep + 'objradec.lst')
    raw_input('edit ok?(y)')
    return get_ra_dec(fn)

def set_ra_dec(fn, ra, dec):
    """
    set the fits fn keyword 'RA' and 'DEC'
    ra : format like '12:34:56.78'
    dec : format like '+23:45:67.89'
    """
    size = len(pyfits.open(fn))
    if size == 1:
        iraf.hedit(images=fn, fields='RA', value=ra, add='Yes', addonly='No',
                   delete='No', verify='No', show='Yes', update='Yes')
        iraf.hedit(images=fn, fields='DEC', value=dec, add='Yes', addonly='No',
                   delete='No', verify='No', show='Yes', update='Yes')
    else:
        for i in range(len(size)):
            iraf.hedit(images=fn + '[%d]' % i, fields='RA', value=ra,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')
            iraf.hedit(images=fn + '[%d]' % i, fields='DEC', value=dec,
                       add='Yes', addonly='No', delete='No', verify='No',
                       show='Yes', update='Yes')

    ######
def standard(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='ca',
                  extinction=extpath, caldir=stdpath)
    std_fitsname = namelst[0]
    stdname, stdmag, stdmagband = standard_star_info(std_fitsname)
    wid, sep = get_band_width_sep(stdname)
    print('<<<<<the standard star is ',stdname,'>>>>>')
    print std_fitsname
    if os.path.isfile('Std'):
        print('remove file Std')
        os.remove('Std')

    iraf.standard(input=std_fitsname, output='Std', samestar=True,
                  beam_switch=False, apertures='', bandwidth=wid,
                  bandsep=sep,  # 30.0  20.0
                  fnuzero=3.6800000000000E-20, extinction=extpath,
                  caldir=stdpath, observatory='ca', interact=True,
                  graphics='stdgraph', cursor='', star_name=stdname,
                  airmass='', exptime='', mag=stdmag, magband=stdmagband,
                  teff='', answer='yes')

    if os.path.isfile('Sens.fits'):
        print('remove file Sens.fits')
        os.remove('Sens.fits')

    iraf.sensfunc(standards='Std', sensitivity='Sens',
                  extinction=extpath, function='spline3', order=15)

    iraf.splot('Sens')
    iraf.flpr()


def standard_star_info(fn):

    objname = pyfits.getval(fn, 'OBJECT')
    objname ,other =objname.split()
    stdlstname = config_path + os.sep + 'standard.lst'
    lst = open(stdlstname).readlines()
    for i in lst:
        compare_name=str(i.split()[0])
        if compare_name == objname:
            stdname=i.split()[1]
            mag = i.split()[2]
            band = i.split()[3]
            return stdname, float(mag), band
    print('can\'t match the object name %s .\nPlease check and '
                   'edit the match file.' % objname)
    webbrowser.open(config_path + os.sep + 'standard.lst')
    raw_input('edit ok?(y)')
    return standard_star_info(fn)

def get_band_width_sep(name):
    if name == 'hd93521' or name == 'feige34':
        return 30.0, 20.0
    else:
        return 'INDEF', 'INDEF'

        ####
def calibrate(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='ca',
                  extinction=extpath, caldir=stdpath)

    for fitname in namelst:
        outname = 'mark_' + fitname
        if os.path.isfile(outname):
            print('remove file ' + outname)
            os.remove(outname)

        iraf.calibrate(input=fitname, output=outname, extinct='yes',
                       flux='yes', extinction=extpath, ignoreaps='yes',
                       sensitivity='Sens', fnu='no')
        iraf.splot(images=outname)
        iraf.flpr()

def main():
    print('<<<<< run the re_corflux.py & correct the flux >>>>>')
    for name in file('cor_lamp.lst'):
        set_airmass('awftb'+name.strip())

    stdlst = open('std.lst').readlines()
    stdlst = ['awftb'+i.strip() for i in stdlst]
    standard(stdlst)

    objlst = open('cor_std.lst').readlines()
    objlst = ['awftb'+i.strip() for i in objlst]
    calibrate(objlst)


if __name__ == '__main__':
    main()
