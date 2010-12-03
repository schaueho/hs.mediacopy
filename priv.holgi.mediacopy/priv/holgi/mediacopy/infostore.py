import copy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from priv.holgi.mediacopy.metainfo import MetaInfo
from priv.holgi.mediacopy.dbmodel import Base, MetaInfoModel

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
        mimodel = self._translate_metainfo_to_metainfomodel(metainfo)
        self._session.add(mimodel)
        self._session.commit()
        self._session.detach(mimodel)

    def _translate_metainfo_to_metainfomodel(self, metainfo):
        ''' Make a new MetaInfoModel object from metainfo '''
    
        keys = metainfo.keys()
        discriminator = self._get_discriminator(metainfo)
        mimodel = MetaInfoModel()
        for key in keys:
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
        
    def get_all_metainfos(self, key, value):
        ''' Return all metainfo objects from the store matching 
        the criteria key=value. Key needs to be of type string. '''
        key = key.lower()
        criteria = { key: value }
        result = self._session.query(MetaInfoModel).filter_by(**criteria).all()
        return result

def make_infostore(dsn):
    ''' Returns an infostore, with possibly empty data '''
    metadata = Base.metadata
    infostore = InfoStore(dsn, metadata)
    return infostore

    
