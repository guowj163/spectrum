#!/usr/bin/env python

import re
import os
import glob
from pyraf import iraf
from astropy.io import fits


script_path = os.path.dirname(os.path.realpath(__file__))  # this script path
config_path = script_path + os.sep + 'config' 
cdherb_file = config_path+os.sep+'cdherb.dat'

def identify():
    iraf.twodspec()
    iraf.longslit()
    iraf.identify(images='Lamp.fits', section='middle column',
                  database='database', coordlist=cdherb_file,
                  nsum=10, match=-3.0, maxfeatures=50, zwidth=100.0,
                  ftype='emission', fwidth=20.0, cradius=7.0, threshold=0.0,
                  minsep=2.0, function='chebyshev', order=6, sample='*',
                  niterate=0, low_reject=3.0, high_reject=3.0, grow=0.0,
                  autowrite='no')
    iraf.flpr()



def reidentify():
    iraf.twodspec()
    iraf.longslit()
    iraf.reidentify(reference='Lamp', images='Lamp', interactive='no',
                    section='column', newaps='yes', override='yes', refit='yes',
                    trace='no', step=10, nsum=10, shift=0.0, search=0.0,
                    nlost=5, cradius=7.0, threshold=0.0, addfeatures='no',
                    coordlist=cdherb_file, match=-3.0,
                    maxfeatures=50, minsep=2.0, database='database')
    iraf.flpr()


def fitcoords():
    iraf.twodspec()
    iraf.longslit()
    iraf.fitcoords(images='Lamp', fitname='Lamp', interactive='yes',
                   combine='no', database='database', deletions='deletions.db',
                   function='chebyshev', xorder=6, yorder=6)


def transform(lst):
    f = open(lst)
    l = f.readlines()
    f.close()

    namelst = ['ftb' + i for i in l]
    outputlst = ['wftb' + i for i in l]
    f = open("temp1.txt", 'w')
    for i in namelst:
        f.write(i + '\n')
    f.close()
    f = open("temp2.txt", 'w')
    for i in outputlst:
        f.write(i + '\n')
    f.close()
    
    iraf.twodspec()
    iraf.longslit(dispaxis=2)
# 
    iraf.transform(input='@temp1.txt', output='@temp2.txt',
                   minput='', moutput='', fitnames='LampLamp',
                   database='database', interptype='spline3',
                   flux='yes')




def combinelamp(lst):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.imcombine(input='%ftb%ftb%@' + lst, output='Lamp', combine='sum',
                   reject='none')
    print('<<<<<combine the lamp & generate the Lamp.fits>>>>>')
    iraf.flpr()

def clear():
    if os.path.isfile('Lamp.fits'):
        os.remove('Lamp.fits')
    
    filelst = glob.glob('wftbcaf*.fits')
    for name in filelst:
        print 'remove ' + name
        os.remove(name)
    print('clear all the previous file')

def main():

    print('<<<<<run the lampcomb_wavelenthcalib.py>>>>>')

    clear()

    combinelamp('lamp.lst')
    
    identify()
    reidentify()
    fitcoords()
    transform('cor_lamp.lst')

if __name__ == '__main__':
    main()



































