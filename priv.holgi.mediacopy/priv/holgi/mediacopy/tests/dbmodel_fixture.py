'''
    dbmodel_fixture.py -- test fixture data.
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
from fixture import DataSet

testpath = os.path.dirname(__file__) 

class ImageMetaInfoModel_Data(DataSet):
    class cimg2448:
        name = u'cimg2448.jpg'
        abspath = unicode(os.path.join(testpath, u'CIMG2448.JPG'))
        exif_datetimeoriginal = u'2010:02:16 14:21:25'
        image_model = u'EX-P700'
        image_make = u'CASIO COMPUTER CO.,LTD '


