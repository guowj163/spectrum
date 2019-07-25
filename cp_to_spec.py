#!/usr/bin/env python
# -*- coding: utf-8 -*-

import re
import os
import glob
import shutil
from astropy.io import fits as pyfits

def rename(name):
    """
    replace the ":" in a file name to "_"
    """
    new_name = name.replace(':', '_')
    print 'rename %s  %s' % (name, new_name)
    os.rename(name, new_name)


def main():
    """
    mv spec file from current dir to spec/
    if dir spec not exist, mkdir spec.
    """

    if not os.path.isdir('spec'):
        print('mkdir spec')
        os.mkdir('spec')
    
    fitsnames = glob.glob('caf*.fits')

    for name in fitsnames:
        rename(name)

    fitsnames = glob.glob('caf*.fits')

    for name in fitsnames:
        obj = pyfits.getval(name, 'OBJECT').lower()
        bia = pyfits.getval(name, 'EXPTIME')
        sli = pyfits.getval(name, 'INSAPID').strip().lower()
        if bia == 0.0 or (sli == 'slit' and ('acq'  not in obj) and ('test'  not in obj)):
            print 'copy %s  spec/' % name
            shutil.copy(name, 'spec'+os.sep+name)

if __name__ == "__main__":
    main()
