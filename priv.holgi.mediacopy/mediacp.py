#!/usr/bin/python
'''
    mediacp.py -- main method for the mediacopy package.
    This file is part of mediacopy.

    Copyright (C) 2010 Holger Schauer <holger.schauer@gmx.de>

    mediacopy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 2 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import os
from optparse import OptionParser
from priv.holgi.mediacopy.utils import logger, unicodify
from priv.holgi.mediacopy.types import get_metainfo
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.filelib import validate_destination, \
    copy_file, walktree, reduce_filename

_destination = os.path.join(os.getenv("HOME"), "Bilder", "Fotos")

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-d', '--destination', dest="destination", 
                      type="string", default=_destination, 
                      help="set destination (default: %s)" % _destination)
    parser.add_option('-D', '--database', dest="database", 
                      type="string", default=_destination, 
                      help="location (path without filename) of database")
    parser.add_option('-e', "--encoding", dest="encoding",
                      action="store_true", help="file name encoding")
    parser.add_option('-f', '--force', dest="force", action="store_true",
                      help="force overwrite")
    parser.add_option('-n', '--noaction', dest="noaction", action="store_true",
                      help="don't perform the action")
    parser.add_option('-u', '--unknown', dest="copyunknown", 
                      action="store_true",
                      help="copy unknown filetypes as well")
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
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
        if options.noaction:
            logger.info("Would copy %s" % filename)
        else:
            if options.verbose:
                logger.info("Would copy %s" % filename)
            copy_file(filename, options.destination,
                      options.force, options.noaction)
            store.put_metainfo(duplicate or get_metainfo(filename))
        copycount = copycount + 1
        return copycount 

    filename = unicodify(filename, options.encoding or 'utf-8')
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

def make_dsn(dblocation):
    dsn = 'sqlite:///'+os.path.join(dblocation, 'mediacopy.db')
    return dsn

def main():
    parser, options, args = parse_options()
    try:
        validate_destination(options.destination)
    except IOError, e:
        parser.print_help()
        raise e

    dsn = make_dsn(options.database or options.destination)
    infostore = make_infostore(dsn)
    result = (0,0,0)
    callback = lambda f,g: handle_copy(f, infostore, options, g)
    (seen, copied, dupes) = walktree(args[0], callback, result)
    print "Saw %s files, copied %s files and ignored %s duplicates" % (seen, copied, dupes)

if __name__ == "__main__":
    main()

