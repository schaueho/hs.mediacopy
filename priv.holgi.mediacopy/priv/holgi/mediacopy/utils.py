''' Provide a simple logging utility. '''

import logging

# create logger
logging.basicConfig()
logger = logging.getLogger("mediacopy")
logger.setLevel(logging.INFO)

