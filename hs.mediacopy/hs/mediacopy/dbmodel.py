'''
    dbmodel.py -- database model for storing media information
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
    __mapper_args__ = {'polymorphic_identity': 'image'}
    exif_datetimeoriginal = Column('exif_datetimeoriginal', Unicode(50))
    image_model = Column('image_model', Unicode(50))
    image_make = Column('image_make', Unicode(50))
