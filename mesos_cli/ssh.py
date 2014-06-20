
import os
import sys

from . import cli
from .master import current as master
from . import slave
from . import task

parser = cli.parser(
    description="SSH into the sandbox of a specific task"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task."""
)

def main():
    cfg, args = cli.init(parser)

    t = master.task(args.task)

    os.execvp("ssh", [
      "ssh",
      "-t",
      slave.host(t.slave).split(":")[0],
      "cd %s && bash" % (t.directory,)
    ])
