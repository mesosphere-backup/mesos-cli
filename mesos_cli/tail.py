
# Should be the first import
import gevent.monkey
gevent.monkey.patch_all()

import functools
import gevent
import itertools
import os

from . import cli
from . import master
from . import slave_file
from . import task

parser = cli.parser(
    description="display the last part of a file"
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

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple files/tasks are being examined"
)

def main():
    cfg, args, m = cli.init(parser)

    tlist = master.tasks(m, args.task)
    for t in tlist:
        s = master.slave(m, t["slave_id"])
        d = task.directory(m, t)
        for f in args.file:
            fobj = slave_file.SlaveFile(s, os.path.join(d, f))

            if not args.q and (len(tlist) > 1 or len(args.file) > 1):
                cli.file_header(s, t, f)

            lines = list(itertools.islice(reversed(fobj), args.n))
            for l in reversed(lines):
                print l
