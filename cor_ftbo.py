#! /usr/bin/env python

import os
import glob
import shutil
from astropy.io import fits as pyfits
from pyraf import iraf

script_path = os.path.dirname(os.path.realpath(__file__))  # this script path
std_path = script_path+os.sep+'standarddir'  # standard star template dir path


def get_trim_sec():
    x1 = 100
    x2 = 1050
    y1 = 350
    y2 = 1500
    return (x1, x2, y1, y2)


def coroverbiastrim(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    x1, x2, y1, y2 = get_trim_sec()
    #print x1, x2, y1, y2S
    iraf.ccdproc(images='@'+lstfile, output='b//@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=False, trim=False, zerocor=True, darkcor=False,
                 flatcor=False, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='', zero='Zero',
                 dark='', flat='', illum='', fringe='', minreplace=1.0,
                 scantype='shortscan', nscan=1, interactive=False,
                 function='chebyshev', order=1, sample='*', naverage=1,
                 niterate=1, low_reject=3.0, high_reject=3.0, grow=1.0)

    iraf.ccdproc(images='b//@'+lstfile, output='tb//@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=False, trim=True, zerocor=False, darkcor=False,
                 flatcor=False, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='',
                 trimsec='[%s:%s,%s:%s]' % (x1, x2, y1, y2), zero='Zero',
                 dark='', flat='', illum='', fringe='', minreplace=1.0,
                 scantype='shortscan', nscan=1, interactive=False,
                 function='chebyshev', order=1, sample='*', naverage=1,
                 niterate=1, low_reject=3.0, high_reject=3.0, grow=1.0)

    iraf.flpr()


def combine_flat(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.flatcombine(input='tb//@'+lstfile, output='Halogen',
                     combine='average', reject='crreject', ccdtype='',
                     process=False, subsets=False, delete=False, clobber=False,
                     scale='mode', statsec='', nlow=1, nhigh=1, nkeep=1,
                     mclip=True, lsigma=3.0, hsigma=3.0, rdnoise='CCDRON',
                     gain='CCDGAIN', snoise=0.0, pclip=-0.5, blank=1.0)
    iraf.twodspec()
    iraf.longslit(dispaxis=2, nsum=1, observatory='ca',
                  extinction='onedstds$kpnoextinct.dat',
                  caldir=std_path+os.sep,
                  interp='poly5')
    iraf.response(calibration='Halogen', normalization='Halogen',
                  response='Resp', interactive=True, threshold='INDEF',
                  sample='*', naverage=1, function='spline3', order=25,
                  low_reject=10.0, high_reject=10.0, niterate=1, grow=0.0,
                  graphics='stdgraph', cursor='')
    iraf.flpr()

def corhalogen(lstfile):
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.ccdproc(images='tb@'+lstfile, output='%ftb%ftb%@'+lstfile,
                 ccdtype='', max_cache=0, noproc=False, fixpix=False,
                 overscan=False, trim=False, zerocor=False, darkcor=False,
                 flatcor=True, illumcor=False, fringecor=False, readcor=False,
                 scancor=False, readaxis='line', fixfile='', biassec='',
                 trimsec='', zero='Zero', dark='', flat='Resp', illum='',
                 fringe='', minreplace=1.0, scantype='shortscan', nscan=1,
                 interactive=False, function='chebyshev', order=1, sample='*',
                 naverage=1, niterate=1, low_reject=3.0, high_reject=3.0,
                 grow=1.0)
    iraf.flpr()




def add_DISPAXIS(filelst):
    iraf.hedit(images='@' + filelst, fields='DISPAXIS',
               value='2', addonly='Yes', delete='No', verify='No', show='Yes', update='Yes')


def del_wrong_keyword(fn):
    """
    delete the keyword CCDSEC, DATASEC, BIASSEC in fits fn, the value of the
    keyword is wrong in caha's data, iraf command ccdproc can not process
    the data.
    """
    def del_keyword(fn, keyword):
        iraf.hedit(images=fn, fields=keyword, value='', add='No', addonly='No',
                   delete='Yes', verify='No', show='Yes', update='Yes')
    keywordlst = ['CCDSEC', 'DATASEC', 'BIASSEC']
    for keyword in keywordlst:
        del_keyword(fn, keyword)






def combinebias(lstfn):
    """
    call iraf command zerocombine, combine bias fits.
    lstfn : lst file name
    type : string
    output file : Zero.fits
    """
    iraf.noao()
    iraf.imred()
    iraf.ccdred()
    iraf.zerocombine(input='@'+lstfn, output='Zero', combine='average',
                     reject='minmax', ccdtype='', process=False, delete=False,
                     clobber=False, scale='none', statsec='', nlow=0, nhigh=1,
                     nkeep=1, mclip=True, lsigma=3.0, hsigma=3.0,
                     rdnoise='CCDRON', gain='CCDGAIN', snoise=0.0, pclip=-0.5,
                     blank=0.0)
    iraf.flpr()



def clear():
    """
    clear the last time running the code genereted the files
    """
    filename = os.listdir(os.getcwd())
    filename = [tmp for tmp in filename if os.path.isfile(tmp) and
                (tmp[0:5] == 'tbcaf' or tmp[0:6] == 'ftbcaf' or
                 tmp == 'Halogen.fits' or tmp == 'Resp.fits' or
                 tmp[0:4] == 'bcaf'or tmp == 'Zero.fits')]

    for i in filename:
        os.remove(i)
    print ('clear all the previous files')




def main():

    print ('<<<<< run the cor_ftbo.py >>>>>')

    clear()

    if os.path.isfile('spec_bias.lst'):
        combinebias('spec_bias.lst')
        print ('<<<<< genereate the Zero.fits >>>>>')
    else:
        print('no spec_bias.lst in ' + os.getcwd())

    
 

    namelst = open('all.lst').readlines()
    for name in namelst:
        del_wrong_keyword(name.strip())
    del_wrong_keyword('Zero.fits')
    add_DISPAXIS('all.lst')

    print('<<<<< correct trim bias overscan >>>>>')
    coroverbiastrim('all.lst')

    print('<<<<< correct flat >>>>>')
    combine_flat('halogen.lst')
    corhalogen('cor_halogen.lst')


if __name__ == '__main__':
    main()
