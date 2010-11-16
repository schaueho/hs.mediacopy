#!/usr/bin/python

from os import getenv, access, path, X_OK, W_OK
import datetime
from optparse import OptionParser

destination = path.join(getenv("HOME"), "Bilder")

def parse_options():
    parser = OptionParser()
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    parser.add_option('-n', '--noaction', dest="noaction", action="store_true",
                      help="don't perform the action")
    parser.add_option('-d', '--destination', dest="destination", 
                      type="string", default=destination, 
                      help="set destination (default: %s)" % destination)
    options, args = parser.parse_args()
    return [parser, options, args]

def validate_destination(dest):
    "Validate that the destination exists and is writable."
    if not(path.exists(dest) and path.isdir(dest) and 
           access(dest, W_OK | X_OK)):
        raise IOError("Destination %s doesn't exist or isn't writable" % dest)
    return True

def main():
    parser, options, args = parse_options()
    try:
        validate_destination(options.destination)
    except IOError, e:
        parser.print_help()
        raise e

if __name__ == "__main__":
    main()

