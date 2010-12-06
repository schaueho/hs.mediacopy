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

    @istest
    def get_discriminator_for_ImageMetaInfo(self):
        imi = imagemetainfo_from_file(self.testfile)
        eq_(self.infostore._get_discriminator(imi), 'image')

    @istest
    def put_metainfo_creates_object_in_db(self):
        imi = imagemetainfo_from_file(self.testfile)
        eq_(len(self.infostore.get_all_metainfos()), 1)
        self.infostore.put_metainfo(imi)
        eq_(len(self.infostore.get_all_metainfos()), 2)

    @istest
    def get_all_metainfos_finds_fixturedata(self):
        eq_(len(self.infostore.get_all_metainfos(discriminator='image')), 1)

        
