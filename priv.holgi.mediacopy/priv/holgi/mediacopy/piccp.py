import os
import EXIF as exif
from priv.holgi.mediacopy.metainfo import MetaInfo

def imagemetainfo_from_file(filename):
    ''' Return an ImageMetaInfo object from file '''
    tags = parse_exif(filename)
    basename = os.path.basename(filename)
    return ImageMetaInfo(basename, filename, exiftags=tags)

def parse_exif(filename):
    ''' Parse exif tag from file '''
    tags = None
    f = open(filename, 'rb')
    try:
        tags = exif.process_file(f)
    except:
        pass
    return tags

class ImageMetaInfo(MetaInfo):
    
    def __init__(self, name, abspath, **kw):
        super(ImageMetaInfo, self).__init__(name, abspath, **kw)
        if not('exiftags' in kw.keys()):
            raise KeyError("Missing exiftags parameter")
        
    def is_similar(self, image):
        ''' Check whether two ImageMetaInfo objects are similar
        We check the name as well as the exif information for now.
        '''
        if (self.name == image.name):
            selftags = self.exiftags.keys()
            othertags = image.exiftags.keys()
            selftags.sort()
            othertags.sort()
            if not(selftags == othertags):
                return False
            for tagname in selftags:
                othervalue=None
                try:
                    othervalue=image.exiftags[tagname]
                except KeyError:
                    return False
                else:
                    if not(self.exiftags[tagname] == othervalue):
                        return False
            return True
        else:
            return False


    
