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
    id = Column('id', Integer, Sequence('metainfo_id_seq'), primary_key=True)
    name = Column('name', String(255))
    abspath = Column('abspath', String)
    discriminator = Column('type', String(20))
    __mapper_args__ = {'polymorphic_on': discriminator}

class ImageMetaInfoModel(MetaInfoModel):
    __mapper_args__ = {'polymorphic_identity': 'image'}
    exif_datetimeoriginal = Column('exif_datetimeoriginal', String(50))
    image_model = Column('image_model', String(50))    
    image_make = Column('image_make', String(50))
