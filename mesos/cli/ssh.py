
import copy
import os
import platform
import sys

from . import cli
from .master import current as master
from . import log
from . import slave
from . import task

parser = cli.parser(
    description="SSH into the sandbox of a specific task"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task."""
).completer = cli.task_completer

def main():
    # There's a security bug in Mavericks wrt. urllib2:
    #     http://bugs.python.org/issue20585
    if platform.system() == "Darwin":
        os.environ["no_proxy"] = "*"

    cfg, args = cli.init(parser)

    t = master.task(args.task)

    cmd = [
        "ssh",
        "-t",
        t.slave.hostname,
        "cd {0} && bash".format(t.directory)
    ]
    if t.directory == "":
        print "warning: the task no longer exists on the target slave. " + \
            "Will not enter sandbox"
        cmd = cmd[:-1]

    log.fn(os.execvp, "ssh", cmd)
