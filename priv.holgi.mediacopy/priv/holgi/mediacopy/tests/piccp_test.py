import copy 
from nose.tools import raises, eq_, istest
from priv.holgi.mediacopy.tests.mediacp_base_test import MediacpTestBase
from priv.holgi.mediacopy.piccp import parse_exif, ImageMetaInfo

class Exif_Test(MediacpTestBase):
    
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

class ImageMetaInfo_Test(MediacpTestBase):
    
    def setUp(self):
        self._setup_testpic()
        
    @istest
    def equal_images_are_similar(self):
        exifmock = {'tag1': 1, 'tag2': 'some string'}
        img = ImageMetaInfo(self.testfilename, self.testfile, exiftags=exifmock)
        img2 = copy.copy(img)
        eq_(img.is_similar(img2), True)

    @istest
    def images_withdifferentexiftags_arent_similar(self):
        exifmock = {'tag1': 1, 'tag2': 'some string'}
        img = ImageMetaInfo(self.testfilename, self.testfile, exiftags=exifmock)
        img2 = copy.copy(img)
        eq_(img.is_similar(img2), True)

    @istest
    def images_withdifferentexiftags_arent_similar(self):
        exifmock = {'tag1': 1, 'tag2': 'some string'}
        img = ImageMetaInfo(self.testfilename, self.testfile, exiftags=exifmock)
        img2 = copy.copy(img)
        img2.exiftags = copy.copy(exifmock)
        img2.exiftags['tag3'] = 'a new tag'
        eq_(img.is_similar(img2), False)
