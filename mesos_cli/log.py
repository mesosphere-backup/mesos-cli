
import logging
import sys

def fatal(msg, code=1):
    logging.error(msg)
    sys.exit(code)
