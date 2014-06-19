
import functools
import itertools
import os
import time

from . import cli
from . import master
from . import slave_file
from . import task

RECHECK = 1

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

files_seen = {}
last_seen = None

def follow(cfg, args):
    global last_seen
    for s, t, fobj, show_header in task.files(
            master.state(cfg.master), args.task, args.file):

        fobj.seek(files_seen.get(fobj.name(), 0))
        if fobj.size() == fobj.tell():
            continue

        if fobj.name() != last_seen and not args.q:
            print "==>%s<==" % (fobj.name(),)

        for l in fobj:
            print l

        files_seen[fobj.name()] = fobj.tell()
        last_seen = fobj.name()

def main():
    global last_seen
    cfg, args, m = cli.init(parser)

    for s, t, fobj, show_header in task.files(m, args.task, args.file):
        if not args.q and show_header:
            print "==>%s<==" % (fobj.name(),)

        lines = list(itertools.islice(reversed(fobj), args.n))
        for l in reversed(lines):
            print l

        files_seen[fobj.name()] = fobj.last_size
        last_seen = fobj.name()

    if args.follow:
        while 1:
            follow(cfg, args)
            time.sleep(RECHECK)
