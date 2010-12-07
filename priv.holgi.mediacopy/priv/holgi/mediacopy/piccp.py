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
                exiftags[mkey] = str(mvalue)
            else:
                exiftags[mkey] = mvalue
    basename = u'%s' % os.path.basename(filename).lower()
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

