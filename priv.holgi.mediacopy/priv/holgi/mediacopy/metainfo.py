

class MetaInfo(object):

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
