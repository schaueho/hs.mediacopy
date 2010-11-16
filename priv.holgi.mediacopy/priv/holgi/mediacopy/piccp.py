#!/usr/bin/python

import os
import EXIF as exif
import shutil
from stat import S_ISDIR, S_ISREG, ST_MODE
from optparse import OptionParser

_destination = os.path.join(os.getenv("HOME"), "Bilder", "new")

def parse_options():
    usage = "usage: %prog [options] souredir"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    parser.add_option('-n', '--noaction', dest="noaction", action="store_true",
                      help="don't perform the action")
    parser.add_option('-d', '--destination', dest="destination", 
                      type="string", default=_destination, 
                      help="set destination (default: %s)" % _destination)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

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

def parse_exif(file):
    "Parse exif tag from file"
    print 'visiting: %s' % file
    f = open(file, 'rb')
    tags = exif.process_file(f)
    try:
        print tags['EXIF DateTimeOriginal']
    except KeyError:
        print "Can't read exif date and time (original)"

def copy_file(file, destination):
    "Copy file to destination"
    shutil.copy2(file, destination)

def main():
    callback = None
    parser, options, args = parse_options()
    try:
        validate_destination(options.destination)
    except IOError, e:
        parser.print_help()
        raise e
    if options.noaction:
        callback = visitfile
    else:
        callback = parse_exif
    walktree(args[0], callback)

if __name__ == "__main__":
    main()

