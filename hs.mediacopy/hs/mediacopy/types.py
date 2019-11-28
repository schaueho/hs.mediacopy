'''
    types.py -- functions to identify and dispatch on media type
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


import magic
from hs.mediacopy.metainfo import MetaInfo, \
    ImageMetaInfo
from hs.mediacopy.dbmodel import MetaInfoModel, \
    ImageMetaInfoModel
from hs.mediacopy.piccp import imagemetainfo_from_file

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
    'image': ImageMetaInfo,
}

def is_knownfiletype(filename):
    ''' Determine if we know how to handle a given file '''
    if get_mimetype(filename) in KNOWN_FILETYPES:
        return True

def get_mimetype(filename):
    ''' Determine the (mime) type of a given file '''
    mime = magic.Magic(mime=True)
    return mime.from_file(filename.encode('utf-8'))

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
