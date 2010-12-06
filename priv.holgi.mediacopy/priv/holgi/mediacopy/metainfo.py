class MetaInfo(object):

    ''' The MetaInfo class provides a generic interface to store
    whatever meta info needs to be stored about a particular media
    object.'''

    def __init__(self, name, abspath, **kw):
        self._infodata = {}
        self.name = name
        self.abspath = abspath
        self.setInfo(**kw)
        
    def setInfo(self, **info):
        """Set parameters of the MetaInfo.

        Note: this will also remove all previously set infodata that
        are not contained in the new list of infodata."""
        if info or self._infodata:
            oldinfo = self._infodata
            self._infodata=info
            # ensure we have all our infodata available as instance attributes
            for key, value in info.items():
                setattr(self, key, value)
            # delete old infodata
            for key in oldinfo:
                if not(key in info):
                    delattr(self, key)

    def keys(self):
        ''' Return the info attributes '''
        return self._infodata.keys()

    def values(self):
        ''' Return the values of the info attributes '''
        return self._infodata.values()

    def __str__(self):
        return "%s:%s#%s" % (self.name, self.abspath, self._infodata)

    def is_similar(self, image):
        ''' Check whether two ImageMetaInfo objects are similar
        We check the name as well as the exif information for now.
        '''
        if (self.name == image.name):
            selftags = self.keys()
            othertags = image.keys()
            selftags.sort()
            othertags.sort()
            if not(selftags == othertags):
                return False
            for tagname in selftags:
                othervalue=None
                try:
                    othervalue=getattr(image, tagname)
                except AttributeError:
                    return False
                else:
                    if not(getattr(self,tagname) == othervalue):
                        return False
            return True
        else:
            return False

class ImageMetaInfo(MetaInfo):
    
    def __init__(self, name, abspath, **kw):
        super(ImageMetaInfo, self).__init__(name, abspath, **kw)
        if not('exiftags' in kw.keys()):
            raise KeyError("Missing exiftags parameter")
        else:
            self.setInfo(**kw['exiftags'])

