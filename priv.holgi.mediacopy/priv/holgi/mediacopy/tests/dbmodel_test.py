from sqlalchemy import *
from sqlalchemy.orm import *
from nose.tools import eq_, istest
from fixture import DataTestCase, SQLAlchemyFixture

from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy import dbmodel
from priv.holgi.mediacopy.tests.dbmodel_fixture import ImageMetaInfoModel_Data


class DbModel_Test(DataTestCase):

    # setup a testdb -- we use a sqlite db in memory
    testdsn = 'sqlite://'
    
    def setUp(self):
        self._make_fixture()
        super(DbModel_Test, self).setUp()
        Session = scoped_session(sessionmaker(bind=self.metadata.bind,
                                              autoflush=True, autocommit=False))
        self.session = Session()

    def tearDown(self):
        self.datapool.teardown()

    def _make_fixture(self):
        # we use our test engine and stuff it under the declarative Base!
        enginekeys = { 'echo': True }
        engine = create_engine(self.testdsn,**enginekeys)
        dbmodel.Base.metadata.bind = engine
        self.metadata = dbmodel.Base.metadata
        self.metadata.create_all(engine)
        dataenv = { 'ImageMetaInfoModel_Data': dbmodel.ImageMetaInfoModel,
                    }
        self.fixture = SQLAlchemyFixture(env=dataenv,engine=self.metadata.bind)
        self.datapool = self.fixture.data()
        self.datapool.setup()
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
    
