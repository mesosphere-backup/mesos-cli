
import argparse
import blessings
import logging
logging.basicConfig()

from . import config
from . import master

def init(parser):
    cfg = config.Config()
    args = parser.parse_args()

    return (cfg, args)

def parser(**kwargs):
    return argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        **kwargs
    )

def header(name):
    term = blessings.Terminal()
    print "==>" + term.red + str(name) + term.white + "<=="
