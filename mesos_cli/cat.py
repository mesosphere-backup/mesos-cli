
import os

from . import cli
from . import master
from . import slave
from . import task

parser = cli.parser(
    description="cat a file from a specific task"
)

parser.add_argument(
    'task', type=str,
    help="ID of the task. Must match a specific task."
)

parser.add_argument(
    'file', type=str, nargs="?", default="stdout",
    help="Path to the file inside the task's sandbox."
)

def main():
    cfg, args, m = cli.init(parser)

    t = master.task(m, args.task)
    s = master.slave(m, t["slave_id"])
    p = os.path.join(task.directory(m, t), args.file)

    for chunk in slave.file(s, p):
        print chunk
