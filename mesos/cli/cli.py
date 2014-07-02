
import argparse
import blessings
import logging
import os

import mesos.cli
from . import config
from .master import current as master
from . import exceptions
from . import log

def init(parser=None):
    cfg = config.Config()
    args = parser.parse_args() if parser else None

    logging.basicConfig(
        level=getattr(logging, cfg.log_level.upper()),
        filename=cfg.log_file
    )

    return (cfg, args)

def parser(**kwargs):
    p = argparse.ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        **kwargs
    )

    p.add_argument(
        "-v", "--version",
        action="version", version="%(prog)s {0}".format(mesos.cli.__version__)
    )
    return p

def header(name):
    term = blessings.Terminal()
    print "==>" + term.red + str(name) + term.white + "<=="

def cmds(short=False):
    def fltr(cmd):
        if not cmd.startswith("mesos-"):
            return False
        if cmd.endswith(".sh"):
            return False
        return True

    cmds = []
    for path in os.environ.get("PATH").split(os.pathsep):
        try:
            cmds += filter(fltr, os.listdir(path))
        except OSError:
            pass

    if short:
        cmds = [x.split("-", 1)[-1] for x in cmds]

    return cmds

def task_completer(prefix, parsed_args, **kwargs):
    return [x.id for x in master.tasks(prefix)]

def slave_completer(prefix, parsed_args, **kwargs):
    return [s.id for s in master.slaves(prefix)]

def file_completer(prefix, parsed_args, **kwargs):
    files = set([])
    split = prefix.rsplit("/", 1)
    base = ""
    if len(split) == 2:
        base = split[0]
    pattern = split[-1]

    for t in master.tasks(parsed_args.task):
        # It is possible for the master to have completed tasks that no longer
        # have files and/or executors
        try:
            for f in t.file_list(base):
                rel = os.path.relpath(f["path"], t.directory)
                if rel.rsplit("/", 1)[-1].startswith(pattern):
                    if f["mode"].startswith("d"):
                        rel += "/"
                    files.add(rel)
        except exceptions.MissingExecutor:
            pass
    return files
