
import argparse
import blessings
import logging
import os
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

def cmds():
    cmds = []
    for path in os.environ.get("PATH").split(os.pathsep):
        try:
            cmds += filter(lambda x: x.startswith("mesos-"), os.listdir(path))
        except OSError:
            pass

    return cmds
