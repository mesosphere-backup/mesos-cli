
import os
import sys

from . import cli
from . import master
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
    cfg, args, m = cli.init(parser)

    t = master.task(m, args.task)
    s = master.slave(m, t["slave_id"])
    d = task.directory(m, t)

    os.execvp("ssh", [
      "ssh",
      "-t",
      slave.host(s).split(":")[0],
      "cd %s && bash" % (d,)
    ])
