import os
from fixture import DataSet

testpath = os.path.dirname(__file__) 

class ImageMetaInfoModel_Data(DataSet):
    class cimg2448:
        name = u'cimg2448.jpg'
        abspath = os.path.join(testpath, 'CIMG2448.JPG')
        exif_datetimeoriginal = u'2010:02:16 14:21:25'
        image_model = u'EX-P700'
        image_make = u'CASIO COMPUTER CO.,LTD '


