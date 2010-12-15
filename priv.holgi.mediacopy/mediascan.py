#!/usr/bin/python

import os
import locale
from optparse import OptionParser
from priv.holgi.mediacopy.utils import logger, unicodify
from priv.holgi.mediacopy.types import get_metainfo
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.filelib import reduce_filename, \
    validate_destination, walktree, print_filename

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-D', '--database', dest="database", 
                      type="string", 
                      help="location (path without filename) of database")
    parser.add_option('-e', "--encoding", dest="encoding",
                      action="store_true", help="file name encoding")
    parser.add_option('-n', "--nowrite", dest="nowrite",
                      action="store_true", help="don't write database")
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

def is_duplicate(store, filename):
    ''' Check whether MetaInfo for filename is already contained in store '''
    basename = reduce_filename(filename)
    if store.find_similar_by_name(basename):
        metainfo = get_metainfo(filename)
        if metainfo:
            result = store.find_similar(metainfo)
            return result
    return False

def make_dsn(dblocation):
    dsn = 'sqlite:///'+os.path.join(dblocation, 'mediacopy.db')
    return dsn
    
def storeinfo_from_dir(sourcedir, dblocation, nowrite, 
                       verbose=False, encoding='utf-8'):
    
    def count_and_store_metainfo(store, filename, counts, encoding='utf-8'):
        ''' Store metainfos and return the number of seen files '''
        (seen, dupes) = counts
        ufilename = unicodify(filename, encoding)
        basename = reduce_filename(ufilename)
        if verbose:
            logger.info("Scanning %s" % basename)
        if is_duplicate(store, ufilename):
            logger.info("Ignoring duplicate %s" % basename)
            dupes = dupes + 1
        else:
            store.put_metainfo(get_metainfo(ufilename))
        seen = seen + 1
        return (seen, dupes)

    if nowrite:
        dsn = 'sqlite://'
    else:
        dsn = 'sqlite:///'+os.path.join(dblocation, 'mediacopy.db')
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
    infostore= storeinfo_from_dir(args[0], options.database or args[0],
                                  options.nowrite,
                                  options.verbose,
                                  options.encoding or 'utf-8')
    show_summary_of_current_mis(infostore, options.verbose)

if __name__ == "__main__":
    main()
