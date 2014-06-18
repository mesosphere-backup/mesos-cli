
# Should be the first import
import gevent.monkey
gevent.monkey.patch_all()

import functools

from . import cli
from . import master

parser = cli.parser(
    description="tail a file inside a task's sandbox"
)

parser.add_argument(
    'task',
    help="ID of the task. May match multiple tasks (or all)"
)

parser.add_argument(
    'file', nargs="*", default=["stdout"],
    help="Path to the file inside the task's sandbox."
)

parser.add_argument(
    '-f', '--follow', action='store_true',
    help="Wait for additional data to be appended to the file."
)

parser.add_argument(
    '-n', default=10, type=int,
    help="Number of lines of the file to tail."
)

def get_file(fn):
    pass

def main():
    cfg, args, m = cli.init(parser)

    for t in master.tasks(m, args.task):
        s = master.slave(m, t["slave_id"])
        d = task.directory(m, t)
        for f in args.file:
            p = os.path.join(d, f)

            fn = functools.partial(slave.file, s, d)



