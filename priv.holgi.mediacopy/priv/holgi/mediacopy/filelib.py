'''
    filelib.py -- file handling functions for the mediacopy package.
    This file is part of mediacopy.

    Copyright (C) 2010 Holger Schauer <holger.schauer@gmx.de>

    mediacopy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
import shutil
from stat import S_ISDIR, S_ISREG, ST_MODE
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy.types import is_knownfiletype

_EXTENSION_TABLE = {
    '.jpg' : '.jpg',
    '.jpeg': '.jpg',
    }


def copy_newfile(filename, destination, copyunknown=False, 
                 overwrite=False, noaction=False):
    ''' Copy file to destination only if we think it is new
    Returns True on successful copying
    '''
    basename = reduce_filename(filename)
    if not(is_knownfiletype(filename)) and not(copyunknown):
        logger.info("Unknown file type, ignoring %s" % filename)
        return False
    similars = find_similar_filenames(destination, basename)
    if similars and not(overwrite):
        logger.info("Similar match found, won't copy %s" % \
                        os.path.join(destination, basename))
        return False
    else:
        return copy_file(filename, destination, overwrite, noaction)

def copy_file(filename, destination, overwrite=False, noaction=False):
    ''' Copy file to destination 
    Returns True on successful copying.
    '''
    basename = os.path.basename(filename)
    if target_exists(destination, basename) and not(overwrite):
        logger.info("Not overwriting existing target file %s" % \
                        os.path.join(destination, basename))
        return False
    else:
        if noaction:
            print "Copy %s to %s" % (filename, destination)
        else:
            shutil.copy2(filename, destination)
        return True

def find_similar_filenames(destination, filename):
    ''' Try to determine if we copied filename to destination before
    '''
    match = []
    existing_targets = get_existing_targets(destination)
    for existing_file in existing_targets.keys():
        if similar_filenames(filename, existing_file):
            match.append(existing_targets[existing_file])
            break
    return match

def get_existing_targets(destination):
    ''' Find all existing targets in destination '''
    result = {}
    def collect_filename(filename):
        ''' Simple helper to collect filenames into result ''' 
        result[os.path.basename(filename)]=filename

    walktree(destination, lambda f: collect_filename(f))
    return result

def similar_filenames(filename1, filename2):
    ''' Check whether two file names are similar 
    '''
    cname1 = reduce_filename(filename1)
    cname2 = reduce_filename(filename2)
    if cname1 == cname2:
        return True
    else:
        return False

def reduce_filename(filename):
    ''' Reduce filename to an internal canonical representation
    A canonical representation is a (unicode) string, consisting
    solely of downcased letters (insofar possible). We also reduce
    filename extensions to canonical versions using a lookup table.
    '''
    return reduce_fileext(os.path.basename(filename).lower())

def reduce_fileext(filename):
    ''' Determine file extension from filename and reduce it
    to a known canonical form
    '''
    (base, ext) = os.path.splitext(filename)
    ext = _EXTENSION_TABLE.get(ext, ext)
    return base + ext

def target_exists(destination, filename):
    ''' Determine whether filename exists at destination '''
    return os.path.exists(os.path.join(destination, filename))
  
def validate_destination(dest):
    ''' Validate that the destination exists and is writable. '''
    if not(os.path.exists(dest) and os.path.isdir(dest) and 
           os.access(dest, os.W_OK | os.X_OK)):
        raise IOError("Destination %s doesn't exist or isn't writable" % dest)
    return True

__unspecified__ = object()
def walktree(top, callback, acc=__unspecified__):
    ''' recursively descend the directory tree rooted at top,
        calling the callback function for each regular file
        'acc' can be used as an additional parameter for
        accumulating results which will be returned.
    '''
    accvalue = None
    if not(acc is __unspecified__):
        accvalue = acc
    for filename in os.listdir(top):
        pathname = os.path.join(top, filename)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            if not(acc is __unspecified__):
                accvalue = walktree(pathname, callback, accvalue)
            else:
                walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            if not(acc is __unspecified__):
                accvalue = callback(pathname, accvalue)
            else:
                callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname
    return accvalue

def print_filename(filename):
    ''' Just print out the name of the file we would visit '''
    print 'visiting: %s' % filename
