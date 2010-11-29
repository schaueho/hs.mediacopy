#!/usr/bin/python

import os
from optparse import OptionParser
from priv.holgi.mediacopy.filelib import validate_destination, \
    copy_file, walktree, print_filename

_destination = os.path.join(os.getenv("HOME"), "Bilder", "Fotos")

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    parser.add_option('-f', '--force', dest="force", action="store_true",
                      help="force overwrite")
    parser.add_option('-n', '--noaction', dest="noaction", action="store_true",
                      help="don't perform the action")
    parser.add_option('-d', '--destination', dest="destination", 
                      type="string", default=_destination, 
                      help="set destination (default: %s)" % _destination)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

def main():
    callback = None
    parser, options, args = parse_options()
    try:
        validate_destination(options.destination)
    except IOError, e:
        parser.print_help()
        raise e
    if options.noaction:
        callback = print_filename
    else:
        callback = lambda f: copy_file(f, options.destination, options.force)
    walktree(args[0], callback)

if __name__ == "__main__":
    main()

