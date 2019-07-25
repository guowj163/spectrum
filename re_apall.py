#! /usr/bin/env python
# -*- coding: utf-8 -*-
"""
Created on Thu Nov  5 16:54:57 2015

@author: zzx
"""
import os
import glob
from pyraf import iraf


def apall(lst):
    iraf.noao()
    iraf.twodspec()
    iraf.apextract(dispaxis=1, database='database')

    for infile in lst:
        laper, raper, back_samp = -7, 7, '-30:-15,15:30'
        while True:

            if os.path.isfile('a'+infile):
                os.remove('a'+infile)
            
            delfile = os.getcwd()+os.sep+'database/ap'+infile[0:-5]
            if os.path.isfile(delfile):
                print('remove ' + delfile)
                os.remove(delfile)

            iraf.apall(input=infile, output='a'+infile, apertures=2,
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

def main():
    print('<<<<< run the re_apall.py & extract the spetrum >>>>>')
    lst = [i.strip() for i in file('cor_lamp.lst')]
    inlst = ['wftb'+i for i in lst]
    apall(inlst)


if __name__ == '__main__':
    main()
