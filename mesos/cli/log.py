
import logging
import sys

debug = logging.debug

def fatal(msg, code=1):
    sys.stdout.write(msg + "\n")
    logging.error(msg)
    sys.exit(code)

def fn(f, *args, **kwargs):
    logging.debug("{0}: {1} {2}".format(repr(f), args, kwargs))
    return f(*args, **kwargs)
