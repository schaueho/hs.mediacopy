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
    for key in EXIFTAGS:
        mkey = key.lower()
        mkey = mkey.replace(' ','_')
        exiftags[mkey] = original_exiftags.get(key, None)
    basename = os.path.basename(filename)
    return ImageMetaInfo(basename, filename, exiftags=exiftags)

def parse_exif(filename):
    ''' Parse exif tag from file '''
    tags = None
    f = open(filename, 'rb')
    try:
        tags = exif.process_file(f)
    except:
        pass
    return tags

