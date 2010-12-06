import magic
from priv.holgi.mediacopy.metainfo import MetaInfo, \
    ImageMetaInfo
from priv.holgi.mediacopy.dbmodel import MetaInfoModel, \
    ImageMetaInfoModel
from priv.holgi.mediacopy.piccp import imagemetainfo_from_file

KNOWN_FILETYPES = [
    'image/jpeg',
    ]

FILETYPES2METAINFO = {
    'image/jpeg': imagemetainfo_from_file,
    }

MICLASS2MIMODELCLASS = {
    'MetaInfo': MetaInfoModel,
    'ImageMetaInfo': ImageMetaInfoModel,
    }

MODELDISCRIMINATOR2MICLASS = {
    'image': ImageMetaInfoModel,
}

def is_knownfiletype(filename):
    ''' Determine if we know how to handle a given file '''
    if get_mimetype(filename) in KNOWN_FILETYPES:
        return True

def get_mimetype(filename):
    ''' Determine the (mime) type of a given file '''
    mime = magic.Magic(mime=True)
    return mime.from_file(filename)

def get_metainfo(filename):
    ''' Return a new instance of MetaInfo or a derivative '''
    filetype = get_mimetype(filename)
    if filetype in FILETYPES2METAINFO:
        return FILETYPES2METAINFO[filetype](filename)

def modelclass_for_mi(metainfo):
    ''' Determine the model class for a given metainfo object '''
    return MICLASS2MIMODELCLASS[metainfo.__class__.__name__]

def miclass_for_model(model):
    ''' Determine the metainfo class for a given metainfo model object '''
    return MODELDISCRIMINATOR2MICLASS.get(model.discriminator, MetaInfo)
