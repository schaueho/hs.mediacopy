''' Provide a simple logging utility. '''

import logging

# create logger
logger = logging.getLogger("mediacopy")
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
