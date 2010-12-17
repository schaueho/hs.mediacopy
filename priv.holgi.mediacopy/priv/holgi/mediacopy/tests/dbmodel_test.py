'''
    dbmodel_test.py -- tests related to the database model.
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

import logging
from sqlalchemy import *
from sqlalchemy.orm import *
from nose.tools import eq_, istest
from fixture import DataTestCase, SQLAlchemyFixture
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy import dbmodel
from priv.holgi.mediacopy.tests.dbmodel_fixture import ImageMetaInfoModel_Data

logging.basicConfig()
logging.getLogger('sqlalchemy.engine').setLevel(logging.DEBUG)

class DbModel_Test(DataTestCase):

    # setup a testdb -- we use a sqlite db in memory
    testdsn = u'sqlite://'
    
    def setUp(self):
        self._make_dbconn()
        self._make_fixture(self.engine)
        super(DbModel_Test, self).setUp()
        Session = scoped_session(sessionmaker(bind=self.metadata.bind,
                                              autoflush=True,
                                              autocommit=False))
        self.session = Session()

    def tearDown(self):
        self.data.teardown()

    def _make_dbconn(self):
        enginekeys = { } # { 'echo': True }
        self.engine = create_engine(self.testdsn,**enginekeys)
        dbmodel.Base.metadata.bind = self.engine
        self.metadata = dbmodel.Base.metadata
        self.metadata.create_all(self.engine)

    def _make_fixture(self, engine):
        # we use our test engine and stuff it under the declarative Base!
        dataenv = { 'ImageMetaInfoModel_Data': dbmodel.ImageMetaInfoModel,
                    }
        self.fixture = SQLAlchemyFixture(env=dataenv,engine=engine)
        self.data = self.fixture.data()
        self.data.setup()
        self.datasets = [ImageMetaInfoModel_Data, ]

    @istest
    def fixture_generates_imagemetainfo(self):
        result = self.session.query(dbmodel.ImageMetaInfoModel).filter_by(name=self.data.ImageMetaInfoModel_Data.cimg2448.name).all()
        eq_(len(result), 1)

    @istest
    def fixture_generates_imagemetainfo_with_expected_attributes(self):
        result = self.session.query(dbmodel.ImageMetaInfoModel).filter_by(name=self.data.ImageMetaInfoModel_Data.cimg2448.name).one()
        assert (result.name and result.abspath and \
                result.exif_datetimeoriginal and \
                result.image_model and result.image_make)
    
