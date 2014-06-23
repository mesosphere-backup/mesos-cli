
import os
import sys

from . import cli

def main():
    if len(sys.argv) == 1:
        cmd = "mesos-help"
    else:
        cmd = "mesos-" + sys.argv[1]

    if cmd in cli.cmds():
        os.execvp(cmd, [cmd] + sys.argv[2:])
    else:
        print "'{}' is not a valid command (or cannot be found)".format(cmd)
        sys.exit(1)

