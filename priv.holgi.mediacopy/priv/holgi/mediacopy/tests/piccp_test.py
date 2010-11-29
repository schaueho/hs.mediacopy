from nose.tools import raises
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase
from priv.holgi.mediacopy.piccp import parse_exif

class Piccp_Test(MediacpTestBase):
    
    def setUp(self):
        self._setup_testpic()

    def tearDown(self):
        pass

    def parse_testpic(self):
        return parse_exif(self.testfile)

    def parseexif_returns_dict_test(self):
        assert isinstance(self.parse_testpic(), dict)

    # exif parsing returns a dictionary of tags which,
    # when printed, give strings
    def parseexif_contains_datetimeoriginal_test(self):
        '''EXIF DateTimeOriginal is required exif data'''
        exiftags = self.parse_testpic()
        assert '%s' % exiftags['EXIF DateTimeOriginal'] == '''2010:02:16 14:21:25'''

    def parseexif_contains_imagemodel_test(self):
        '''Image Model is required data'''
        exiftags = self.parse_testpic()
        assert '%s' % exiftags['Image Model'] == '''EX-P700'''

    def parseexif_contains_imagemake_test(self):
        '''Image Make is required data'''
        exiftags = self.parse_testpic()
        print exiftags['Image Make']
        assert '%s' % exiftags['Image Make'] == '''CASIO COMPUTER CO.,LTD '''
