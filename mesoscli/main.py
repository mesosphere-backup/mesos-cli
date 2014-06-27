
import os
import sys

from . import cli
from . import log

def main():
    if len(sys.argv) == 1:
        cmd = "mesos-help"
    else:
        cmd = "mesos-" + sys.argv[1]

    if cmd in cli.cmds():
        log.fn(os.execvp, cmd, [cmd] + sys.argv[2:])
    else:
        log.fatal("'{}' is not a valid command (or cannot be found)".format(cmd))
