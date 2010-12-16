'''
    infostore.py -- fassade to store media information
    This file is part of mediacopy.

    Copyright (C) 2010 Holger Schauer <holger.schauer@gmx.de>

    mediacopy is free software: you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation, either version 3 of the License, or
    (at your option) any later version.

    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with this program.  If not, see <http://www.gnu.org/licenses/>.
'''

import copy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from priv.holgi.mediacopy import dbmodel
from priv.holgi.mediacopy.utils import logger
from priv.holgi.mediacopy.types import modelclass_for_mi, \
    miclass_for_model, get_metainfo

class InfoStore(object):
    ''' An InfoStore stores meta info about media objects
    It abstracts away the database by providing a fassade to
    lower level dbstuff.
    '''
    
    def __init__(self, dsn, metadata, **enginekeys):
        self._engine = create_engine(dsn, **enginekeys)
        self._metadata = metadata
        self._metadata.bind = self._engine
        self._metadata.create_all(self._engine, checkfirst=True)
        smaker = sessionmaker(bind=self._engine,
                              autocommit=True,
                              autoflush=True)
        self._getSession = scoped_session(smaker)
        
    @property
    def _session(self):
        return self._getSession()

    def put_metainfo(self, metainfo):
        ''' Put metainfo as a new info object into store '''
        if not(metainfo): return
        mimodel = self._translate_metainfo_to_metainfomodel(metainfo)
        self._session.begin()
        self._session.add(mimodel)
        self._session.commit()
        self._session.close()

    def _translate_metainfo_to_metainfomodel(self, metainfo):
        ''' Make a new MetaInfoModel object from metainfo '''
    
        keys = metainfo.keys()
        discriminator = self._get_discriminator(metainfo)
        mimodel = modelclass_for_mi(metainfo)()
        allkeys = ['name','abspath'] + keys
        for key in allkeys:
            logger.debug('Adding key %s -> %s' % (key, getattr(metainfo, key)))
            setattr(mimodel, key, getattr(metainfo, key))
        mimodel.discriminator = discriminator
        return mimodel
        
    def _get_discriminator(self, metainfo):
        ''' Returns a discriminator from the class name of metainfo 
        Assumes that the classname of metainfo has a specific suffix.'''
        suffix = 'metainfo'
        klassname = copy.copy(metainfo.__class__.__name__).lower()
        if klassname.endswith(suffix):
            return klassname[:-len(suffix)]
        else:
            raise ValueError("Can't determine discriminator from %s" % metainfo)
        
    def get_all_metainfos(self, **criteria):
        ''' Return all metainfo objects from the store matching 
        the criteria key=value. Key needs to be of type string. '''
        result = []
        dbresult = self._session.query(dbmodel.MetaInfoModel).filter_by(**criteria).all()
        if len(dbresult) > 0:
            result = [ self._translate_metainfomodel_to_metainfo(model) for model in dbresult ]
        return result

    def _translate_metainfomodel_to_metainfo(self, model):
        ''' Make a new MetaInfo object from model '''
    
        ignored = ['id','name','abspath', '_sa_class_manager', 'discriminator']
        modelklass = model.__class__
        attribs = [key for key in modelklass.__dict__.keys() \
                       if (not(key in ignored) and \
                               not(key.startswith('__')))]
        metainfo = miclass_for_model(model)(model.name, model.abspath)
        info = dict([(attrib,getattr(model,attrib)) for attrib in attribs])
        metainfo.setInfo(**info)
        metainfo.id = model.id
        return metainfo

    def find_similar(self, metainfo):
        ''' Find a MetaInfo in store that is similar to metainfo '''
        dupecands = self.get_all_metainfos(name=metainfo.name)
        if len(dupecands) > 0:
            for candidate in dupecands:
                if metainfo.is_similar(candidate):
                    return candidate
        return None

    def find_similar_by_name(self, name):
        ''' Find a MetaInfo in store that is similar according to name '''
        dupecands = self.get_all_metainfos(name=name)
        return dupecands

def make_infostore(dsn):
    ''' Returns an infostore, with possibly empty data '''
    metadata = dbmodel.Base.metadata
    infostore = InfoStore(dsn, metadata)
    return infostore
