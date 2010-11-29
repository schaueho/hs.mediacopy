from nose.tools import raises, eq_, istest
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase
from priv.holgi.mediacopy.piccp import parse_exif

class Piccp_Test(MediacpTestBase):
    
    def setUp(self):
        self._setup_testpic()

    def tearDown(self):
        pass

    def parse_testpic(self):
        return parse_exif(self.testfile)

    @istest
    def parseexif_returns_dict(self):
        assert isinstance(self.parse_testpic(), dict)

    # exif parsing returns a dictionary of tags which,
    # when printed, give strings
    @istest
    def parseexif_contains_datetimeoriginal(self):
        '''EXIF DateTimeOriginal is required exif data'''
        exiftags = self.parse_testpic()
        eq_('%s' % exiftags['EXIF DateTimeOriginal'], '''2010:02:16 14:21:25''')

    @istest
    def parseexif_contains_imagemodel(self):
        '''Image Model is required data'''
        exiftags = self.parse_testpic()
        eq_('%s' % exiftags['Image Model'], '''EX-P700''')

    @istest
    def parseexif_contains_imagemake(self):
        '''Image Make is required data'''
        exiftags = self.parse_testpic()
        eq_('%s' % exiftags['Image Make'], '''CASIO COMPUTER CO.,LTD ''')
