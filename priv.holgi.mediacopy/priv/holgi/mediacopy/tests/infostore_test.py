'''
    infostore_test.py -- tests related to the infostore.
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

from nose.tools import istest, eq_
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase
from priv.holgi.mediacopy.tests.dbmodel_test import DbModel_Test
from priv.holgi.mediacopy.infostore import make_infostore
from priv.holgi.mediacopy.piccp import ImageMetaInfo, imagemetainfo_from_file
from priv.holgi.mediacopy.dbmodel import ImageMetaInfoModel

class InfoStore_Test(DbModel_Test, MediacpTestBase):
    
    def setUp(self):
        self.infostore = make_infostore(self.testdsn)
        self._make_fixture(self.infostore._engine)
        self.session = self.infostore._session
        self._setup_testpic()
        super(DbModel_Test, self).setUp()

    def tearDown(self):
        super(DbModel_Test, self).tearDown()

    @istest
    def get_discriminator_for_ImageMetaInfo(self):
        imi = imagemetainfo_from_file(self.testfile)
        eq_(self.infostore._get_discriminator(imi), u'image')

    @istest
    def put_metainfo_creates_object_in_db(self):
        imi = imagemetainfo_from_file(self.testfile)
        name = u'new'+imi.name.lower()
        imi.name = name
        self.infostore.put_metainfo(imi)
        result = self.infostore.get_all_metainfos(name=name)
        eq_(len(result), 1)
        eq_(result[0].name, name)
        eq_(result[0].exif_datetimeoriginal, 
            str(imi.exif_datetimeoriginal))
        eq_(result[0].image_make, 
            str(imi.image_make))
        eq_(result[0].image_model, 
            str(imi.image_model))

    @istest
    def get_all_metainfos_finds_fixturedata(self):
        result = self.infostore.get_all_metainfos()
        eq_(len(result), 1)

    @istest
    def get_all_metainfos_finds_imagemetainfomodeldata_from_fixture(self):
        imi = self.data.ImageMetaInfoModel_Data.cimg2555
        result = self.infostore.get_all_metainfos(discriminator=u'image', 
                                                  name=imi.name)
        eq_(len(result), 1)
        eq_(isinstance(result[0], ImageMetaInfo), True)
        eq_(result[0].exif_datetimeoriginal, 
            str(self.data.ImageMetaInfoModel_Data.cimg2555.exif_datetimeoriginal))
        eq_(result[0].image_make, 
            str(imi.image_make))
        eq_(result[0].image_model, 
            str(imi.image_model))

    @istest
    def find_similar_finds_result_after_put(self):
        imi = imagemetainfo_from_file(self.testfile)
        self.infostore.put_metainfo(imi)
        eq_(isinstance(self.infostore.find_similar(imi), ImageMetaInfo), True)
        
