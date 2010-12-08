from sqlalchemy import *
from sqlalchemy.orm import *
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.schema import DDL

Base = declarative_base()

''' SQLalchemy ORM models for usage with MetaInfo objects 
MetaInfo objects are basically DTOs for the models here.
The code relies on a relation between DTO class names and
strings used as discriminators: DTO class names get stripped
of any 'MetaInfo' suffix.
'''

class MetaInfoModel(Base):
    __tablename__ = 'metainfo'
    id = Column('id', Integer, Sequence('metainfo_id_seq'), 
                primary_key=True)
    name = Column('name', Unicode(255), index=True)
    abspath = Column('abspath', Unicode)
    discriminator = Column('type', Unicode(20), index=True)
    __mapper_args__ = {'polymorphic_on': discriminator}

class ImageMetaInfoModel(MetaInfoModel):
    __mapper_args__ = {'polymorphic_identity': u'image'}
    exif_datetimeoriginal = Column('exif_datetimeoriginal', Unicode(50))
    image_model = Column('image_model', Unicode(50))    
    image_make = Column('image_make', Unicode(50))
