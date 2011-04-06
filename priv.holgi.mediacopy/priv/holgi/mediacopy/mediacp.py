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
import sys
from optparse import OptionParser
from priv.holgi.mediacopy.utils import make_dsn
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.applogic import mediacopy_directory
from priv.holgi.mediacopy.filelib import validate_destination
    

_destination = os.path.join(os.getenv("HOME"), "Bilder", "Fotos")
_default_encoding=sys.getfilesystemencoding() or 'utf-8'

def parse_options():
    usage = "usage: %prog [options] sourcedir destinationdir"
    parser = OptionParser(usage=usage)
    parser.add_option('-D', '--database', dest="database", 
                      type="string", default=_destination, 
                      help="(location of) destination database holding metadata")
    parser.add_option('-e', "--encoding", dest="encoding",
                      type="string", default=_default_encoding,
                      help="file name encoding")
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
    if len(args) != 2:
        parser.error("incorrect number of arguments")
    return [parser, options, args]

def main():
    parser, options, args = parse_options()
    try:
        validate_destination(args[1])
    except IOError, e:
        parser.print_help()
        raise e

    result = (0,0,0)
    dsn = make_dsn(options.database or options.destination)
    infostore = make_infostore(dsn)
    (seen, copied, dupes) = mediacopy_directory(args[0], args[1], infostore, options, result)
    print "Saw %s files, copied %s files and ignored %s duplicates" % (seen, copied, dupes)

if __name__ == "__main__":
    main()

