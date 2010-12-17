'''
    piccp.py -- functions for handling of pictures.
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
import EXIF as exif
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy.metainfo import ImageMetaInfo

EXIFTAGS = [
    'EXIF DateTimeOriginal',
    'Image Model',
    'Image Make',
    ]

def imagemetainfo_from_file(filename):
    ''' Return an ImageMetaInfo object from file '''
    exiftags = {}
    original_exiftags = parse_exif(filename)
    if original_exiftags:
        for key in EXIFTAGS:
            mkey = key.lower()
            mkey = mkey.replace(' ','_')
            mvalue = original_exiftags.get(key, None)
            if mvalue:
                exiftags[mkey] = unicode(mvalue)
            else:
                exiftags[mkey] = mvalue
    basename = os.path.basename(filename).lower()
    return ImageMetaInfo(basename, filename, exiftags=exiftags)

def parse_exif(filename):
    ''' Parse exif tag from file '''
    tags = {}
    fhandle = open(filename, 'rb')
    try:
        tags = exif.process_file(fhandle)
    except:
        fhandle.close()
    return tags

