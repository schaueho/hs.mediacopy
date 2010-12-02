import magic
from priv.holgi.mediacopy.piccp import imagemetainfo_from_file

KNOWN_FILETYPES = [
    'image/jpeg',
    ]

FILETYPES2METAINFO = {
    'image/jpeg': imagemetainfo_from_file,
    }


def is_knownfiletype(filename):
    ''' Determine if we know how to handle a given file '''
    if get_mimetype(filename) in KNOWN_FILETYPES:
        return True

def get_mimetype(filename):
    ''' Determine the (mime) type of a given file '''
    mime = magic.Magic(mime=True)
    return mime.from_file(filename)


