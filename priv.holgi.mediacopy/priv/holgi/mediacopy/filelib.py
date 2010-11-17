import os
import shutil
from stat import S_ISDIR, S_ISREG, ST_MODE

def validate_destination(dest):
    "Validate that the destination exists and is writable."
    if not(os.path.exists(dest) and os.path.isdir(dest) and 
           os.access(dest, os.W_OK | os.X_OK)):
        raise IOError("Destination %s doesn't exist or isn't writable" % dest)
    return True

def walktree(top, callback):
    '''recursively descend the directory tree rooted at top,
       calling the callback function for each regular file'''

    for f in os.listdir(top):
        pathname = os.path.join(top, f)
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

def print_filename(file):
    ''' Just print out the name of the file we would visit '''
    print 'visiting: %s' % file

def copy_file(file, destination):
    "Copy file to destination"
    shutil.copy2(file, destination)
