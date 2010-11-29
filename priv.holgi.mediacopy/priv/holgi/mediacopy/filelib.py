import os
import shutil
from stat import S_ISDIR, S_ISREG, ST_MODE

_EXTENSION_TABLE = {
    '.jpg' : '.jpg',
    '.jpeg': '.jpg',
    '.mpg' : '.mpeg',
    '.mpeg': '.mpeg',
    }

def validate_destination(dest):
    ''' Validate that the destination exists and is writable. '''
    if not(os.path.exists(dest) and os.path.isdir(dest) and 
           os.access(dest, os.W_OK | os.X_OK)):
        raise IOError("Destination %s doesn't exist or isn't writable" % dest)
    return True

def walktree(top, callback):
    ''' recursively descend the directory tree rooted at top,
        calling the callback function for each regular file
    '''
    for filename in os.listdir(top):
        pathname = os.path.join(top, filename)
        mode = os.stat(pathname)[ST_MODE]
        if S_ISDIR(mode):
            # It's a directory, recurse into it
            walktree(pathname, callback)
        elif S_ISREG(mode):
            # It's a file, call the callback function
            callback(pathname)
        else:
            # Unknown file type, print a message
            print 'Skipping %s' % pathname

def print_filename(filename):
    ''' Just print out the name of the file we would visit '''
    print 'visiting: %s' % filename

def copy_file(filename, destination, overwrite=False):
    ''' Copy file to destination '''
    shutil.copy2(filename, destination)

def similar_filenames(filename1, filename2):
    ''' Check whether two file names are similar 
    Assumes that filenames are reduced to their basenames already.
    '''
    cname1 = reduce_filename(filename1)
    cname2 = reduce_filename(filename2)
    if cname1 == cname2:
        return True
    else:
        return False

def reduce_fileext(filename):
    ''' Determine file extension from filename and reduce it
    to a known canonical form'''
    (base, ext) = os.path.splitext(filename)
    ext = _EXTENSION_TABLE.get(ext, ext)
    return base + ext

def reduce_filename(filename):
    ''' Reduce filename to an internal canonical representation
    A canonical representation is a (unicode) string, consisting
    solely of downcased letters (insofar possible). We also reduce
    filename extensions to canonical versions using a lookup table.'''
    return reduce_fileext(filename.lower())
  
