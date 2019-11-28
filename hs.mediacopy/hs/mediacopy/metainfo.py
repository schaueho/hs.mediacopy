'''
    metainfo.py -- abstraction of media meta information
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
            for key, value in list(info.items()):
                setattr(self, key, value)
            # delete old infodata
            for key in oldinfo:
                if not(key in info):
                    delattr(self, key)

    def keys(self):
        ''' Return the info attributes '''
        return list(self._infodata.keys())

    def values(self):
        ''' Return the values of the info attributes '''
        return list(self._infodata.values())

    def __str__(self):
        return "%s:%s#%s" % (self.name, self.abspath, self._infodata)

    def is_similar(self, other):
        ''' Check whether two MetaInfo objects are similar
        We check the name as well as the exif information for now.
        '''
        if (self.name == other.name):
            selftags = list(self.keys())
            othertags = list(other.keys())
            selftags.sort()
            othertags.sort()
            if not(selftags == othertags):
                return False
            for tagname in selftags:
                othervalue=None
                try:
                    othervalue=getattr(other, tagname)
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
        try:
            self.setInfo(**kw['exiftags'])
        except KeyError:
            pass
