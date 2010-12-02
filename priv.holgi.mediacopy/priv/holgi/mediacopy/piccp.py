import EXIF as exif

def parse_exif(file):
    "Parse exif tag from file"
    tags = None
    f = open(file, 'rb')
    try:
        tags = exif.process_file(f)
    except:
        pass
    return tags

class ImageMetaInfo(object):
    
    def __init__(self, name, abspath, exiftags={}):
        self.name = name
        self.abspath = abspath
        self.exiftags = exiftags

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

