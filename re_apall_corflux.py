#! /usr/bin/env python
# -*- coding: utf-8 -*-


import os
from pyraf import iraf
from astropy.io import fits as pyfits
from func import script_path
import func

stdpath = func.std_path+os.sep
extpath = func.extinction_file


def apall(ilst, olst):
    iraf.noao()
    iraf.twodspec()
    iraf.apextract(dispaxis=1, database='database')
    for i, infile in enumerate(ilst):
        outfile = olst[i]
        laper, raper, back_samp = -7, 7, '-30:-15,15:30'
        while True:
            if os.path.isfile(outfile):
                print('remove ' + outfile)
                os.remove(outfile)

            delfile = os.getcwd()+os.sep+'database/ap'+infile[0:-5]
            if os.path.isfile(delfile):
                print('remove ' + delfile)
                os.remove(delfile)
            iraf.apall(input=infile, output=outfile, apertures=2,
                       format='multispec', references='', profiles='',
                       interactive=True, find=True, recenter=True,
                       resize=False, edit=True, trace=True, fittrace=True,
                       extract=True, extras=True, review=True, line='INDEF',
                       nsum=10, lower=laper, upper=raper, apidtable='',
                       b_function='chebyshev', b_order=2, b_sample=back_samp,
                       b_naverage=-25, b_niterate=1, b_low_reject=3.0,
                       b_high_reject=3.0, b_grow=0.0, width=5.0, radius=10.0,
                       threshold=0.0, nfind=2, minsep=5.0, maxsep=100000.0,
                       order='increasing', aprecenter='', npeaks='INDEF',
                       shift=True, llimit='INDEF', ulimit='INDEF', ylevel=0.1,
                       peak=True, bkg=True, r_grow=0.0, avglimits=False,
                       t_nsum=20, t_step=10, t_nlost=3, t_function='legendre',
                       t_order=12, t_sample='*', t_naverage=1, t_niterate=1,
                       t_low_reject=3.0, t_high_reject=3.0, t_grow=0.0,
                       background='median', skybox=1, weights='none',
                       pfit='fit1d', clean=True, saturation='INDEF',
                       readnoise='CCDRON', gain='CCDGAIN', lsigma=4.0, usigma=4.0,
                       nsubaps=1)

            iraf.flpr()
            getval = raw_input(('Are you need repeat apall,'
                                'may be clean should be close(r/n)'))
            if getval != 'r':
                break




def get_band_width_sep(fn):
    name = func.sname(fn)
    if name == 'hd93521' or name == 'feige34':
        return 30.0, 20.0
    else:
        return 'INDEF', 'INDEF'


def standard(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory=func.obs.name,
                  extinction=extpath, caldir=stdpath)
    stdnamelst = []
    for std_fitsname in namelst:
        stdname, stdmag, stdmagband = func.standard_star_info(std_fitsname)
        print('the standard star is ' + stdname, 'green')
        stdnamelst.append(std_fitsname)
    stdnamestr = func.to_str(stdnamelst)

    if os.path.isfile('Std'):
        print('remove file Std')
        os.remove('Std')
        
    wid, sep = get_band_width_sep(namelst[0])
    iraf.standard(input=stdnamestr, output='Std', samestar=True,
                  beam_switch=False, apertures='', bandwidth=wid,
                  bandsep=sep,  # 30.0  20.0
                  fnuzero=3.6800000000000E-20, extinction=extpath,
                  caldir=stdpath, observatory=func.obs.name, interact=True,
                  graphics='stdgraph', cursor='', star_name=stdname,
                  airmass='', exptime='', mag=stdmag, magband=stdmagband,
                  teff='', answer='yes')
    if os.path.isfile('Sens.fits'):
        print('remove file Sens.fits')
        os.remove('Sens.fits')
    iraf.sensfunc(standards='Std', sensitivity='Sens',
                  extinction=extpath, function='spline3', order=15)
    iraf.splot('Sens')


def calibrate(namelst):
    iraf.noao()
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory=func.obs.name,
                  extinction=extpath, caldir=stdpath)
    for fitname in namelst:
        outname = 'mark_' + fitname
        if os.path.isfile(outname):
            print('remove file ' + outname)
            os.remove(outname)
        stdfitname = 'Sens'
        iraf.calibrate(input=fitname, output=outname, extinct='yes',
                       flux='yes', extinction=extpath, ignoreaps='yes',
                       sensitivity=stdfitname, fnu='no')
        iraf.splot(images=outname)


def main():
    print('<<<<< run the re_apall.py & extract the spetrum >>>>>')
    lst = [i.strip() for i in file('cor_lamp.lst')]
    ilst = ['wftb'+i for i in lst]
    olst = ['awftb'+i for i in lst]
    apall(ilst, olst)
    
    # for name in file('cor_lamp.lst'):
    #     func.set_airmass('awftb'+name.strip())
    # stdlst = open('std.lst').readlines()
    # stdlst = ['awftb'+i.strip() for i in stdlst]
    # standard(stdlst)
    # objlst = open('cor_std.lst').readlines()
    # objlst = ['awftb'+i.strip() for i in objlst]
    # calibrate(objlst)



if __name__ == '__main__':
    main()
