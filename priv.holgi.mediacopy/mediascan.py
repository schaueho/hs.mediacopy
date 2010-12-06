#!/usr/bin/python

import os
from optparse import OptionParser
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy.types import get_metainfo
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.filelib import reduce_filename, \
    validate_destination, walktree

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    parser.add_option('-n', "--don't write database", dest="nowrite",
                      action="store_true", help="verbose logging")
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

def storeinfo_from_dir(sourcedir, nowrite):
    
    def count_and_store_metainfo(store, filename, counts):
        ''' Store metainfos and return the number of seen files '''
        (seen, dupes) = counts
        basename = reduce_filename(filename)
        result = store.get_all_metainfos(name=basename)
        if len(result) >= 1:
            dupes = dupes + 1
            logger.info("Ignoring duplicate %s" % basename)
        else:
            store.put_metainfo(get_metainfo(filename))
        seen = seen + 1
        return (seen, dupes)

    if nowrite:
        dsn = 'sqlite://'
    else:
        dsn = 'sqlite:///'+sourcedir+'mediacopy.db'
    infostore = make_infostore(dsn)

    callback  = lambda f,g : count_and_store_metainfo(infostore, f, g)
    (seen, dupes) = walktree(sourcedir, callback, (0, 0))
    print "Saw %s files and %s duplicates" % (seen, dupes)
    return infostore

def show_summary_of_current_mis(infostore, verbose):
    current_mis = infostore.get_all_metainfos()
    if verbose:
        for mi in current_mis:
            logger.info("Looking at: %s" % mi.name)
    print "Stored metainfo items: %s" % len(current_mis)

def main():
    parser, options, args = parse_options()
    try:
        validate_destination(args[0])
    except IOError, e:
        parser.print_help()
        raise e
    infostore= storeinfo_from_dir(args[0], options.nowrite)
    show_summary_of_current_mis(infostore, options.verbose)

if __name__ == "__main__":
    main()
