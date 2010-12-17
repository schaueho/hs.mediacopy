#!/usr/bin/python
'''
    mediascan.py -- scanning utility for the mediacopy.
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
import sys
from optparse import OptionParser
from priv.holgi.mediacopy.utils import logger, unicodify
from priv.holgi.mediacopy.types import get_metainfo
from priv.holgi.mediacopy.infostore import make_infostore, find_metainfo
from priv.holgi.mediacopy.applogic import find_metainfo, store_metainfo
from priv.holgi.mediacopy.filelib import reduce_filename, \
    validate_destination, walktree, print_filename

_default_encoding=sys.getfilesystemencoding() or 'utf-8'

def show_summary_of_current_mis(infostore, options):
    current_mis = infostore.get_all_metainfos()
    if options.verbose:
        for mi in current_mis:
            logger.info("Looking at: %s" % mi.name)
    print "Stored metainfo items: %s" % len(current_mis)

def parse_options():
    usage = "usage: %prog [options] sourcedir"
    parser = OptionParser(usage=usage)
    parser.add_option('-D', '--database', dest="database", 
                      type="string", 
                      help="location (path without filename) of database")
    parser.add_option('-e', "--encoding", dest="encoding",
                      type="string", help="file name encoding",
                      default=_default_encoding)
    parser.add_option('-n', "--nowrite", dest="nowrite",
                      action="store_true", help="don't write database")
    parser.add_option('-v', '--verbose', dest="verbose", action="store_true",
                      help="verbose logging")
    options, args = parser.parse_args()
    if len(args) != 1:
        parser.error("incorrect number of arguments")
    return [parser, options, args]
 
def main():
    parser, options, args = parse_options()
    try:
        validate_destination(args[0])
    except IOError, e:
        parser.print_help()
        raise e

    dsn = make_dsn((options.nowrite and '') or options.destination)
    infostore = make_infostore(dsn)
    (seen, dupes) = storeinfo_from_dir(infostore, args[0], options, (0,0))
    show_summary_of_current_mis(infostore, options)

if __name__ == "__main__":
    main()
