'''
    utils.py -- common utilities for other functions/methods.
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
import logging

# create logger
logging.basicConfig()
logger = logging.getLogger("mediacopy")
logger.setLevel(logging.INFO)


def unicodify(string, encoding='utf-8'):
    result = None
    try:
        result = unicode(string)
    except UnicodeDecodeError:
        try:
            result = unicode(string, encoding)
        except UnicodeDecodeError:
            result = string.decode(encoding)
    return result

def make_dsn(dblocation):
    if (os.path.exists(dest) and os.path.isdir(dest)):
        dsn = 'sqlite:///'+os.path.join(dblocation, 'mediacopy.db')
    else:
        if (os.path.exists(dblocation) and os.path.isfile(dblocation)):
            dsn = 'sqlite:///'+dblocation
        else:
            raise IOError("Database location %s doesn't exist" % dblocation)
    return dsn
