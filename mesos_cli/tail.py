
# Should be the first import
import gevent.monkey
gevent.monkey.patch_all()

import functools
import gevent
import os

from . import cli
from . import master
from . import slave_file
from . import task

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

def get_file(fobj, follow=False, n=10):
    while 1:
        for l in fobj

def main():
    cfg, args, m = cli.init(parser)

    for t in master.tasks(m, args.task):
        s = master.slave(m, t["slave_id"])
        d = task.directory(m, t)
        for f in args.file:
            fobj = slave_file.SlaveFile(s, os.path.join(d, f))

            gevent.spawn(get_file, fobj, args.follow, args.n)
