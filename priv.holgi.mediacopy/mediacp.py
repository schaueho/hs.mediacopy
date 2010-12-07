#!/usr/bin/python

import os
from optparse import OptionParser
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy.types import get_metainfo
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.filelib import validate_destination, \
    copy_file, walktree, reduce_filename

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
    parser.add_option('-u', '--unknown', dest="copyunknown", 
                      action="store_true",
                      help="copy unknown filetypes as well")
    parser.add_option('-d', '--destination', dest="destination", 
                      type="string", default=_destination, 
                      help="set destination (default: %s)" % _destination)
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

def mi_if_duplicate(store, filename):
    ''' Check whether MetaInfo for filename is already contained in store '''
    basename = reduce_filename(filename)
    if store.find_similar_by_name(basename):
        metainfo = get_metainfo(filename)
        if metainfo:
            result = store.find_similar(metainfo)
            return metainfo
    return False

def handle_copy(filename, store, options, result):
    (filecount, copycount, dupecount) = result

    def copy_and_store(filename, store, options, copycount, duplicate=None):
        ''' Copy file to destination and store metainfo '''
        copy_file(filename, options.destination,
                  options.force, options.noaction)
        copycount = copycount + 1
        store.put_metainfo(duplicate or get_metainfo(filename))
        return copycount 

    filecount = filecount + 1
    duplicate = mi_if_duplicate(store, filename)
    if duplicate:
        dupecount = dupecount + 1
        if options.force:
            logger.info("Force copy of duplicate %s" % filename)
            copycount = copy_and_store(filename, store, options, copycount, duplicate)
        else:
            logger.info("Ignoring duplicate %s" % filename)
    else:
        copycount = copy_and_store(filename, store, options, copycount)
    return (filecount, copycount, dupecount)


def main():
    parser, options, args = parse_options()
    try:
        validate_destination(options.destination)
    except IOError, e:
        parser.print_help()
        raise e

    dsn = 'sqlite:///'+os.path.join(options.destination, 'mediacopy.db')
    infostore = make_infostore(dsn)
    result = (0,0,0)
    callback = lambda f,g: handle_copy(f, infostore, options, g)
    (seen, copied, dupes) = walktree(args[0], callback, result)
    print "Saw %s files, copied %s files and ignored %s duplicates" % (seen, copied, dupes)

if __name__ == "__main__":
    main()

