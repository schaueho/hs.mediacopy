''' Provide a simple logging utility. '''

import logging

# create logger
logging.basicConfig()
logger = logging.getLogger("mediacopy")
logger.setLevel(logging.INFO)


def unicodify(string, encoding='utf-8'):
    result = None
    try:
        result = unicode(string)
    except UnicodeDecodeError:
        try:
            result = unicode(string, encoding)
        except UnicodeDecodeError:
            result = string.decode(encoding)
    return result
