
import itertools
import os

from . import cli
from . import master
from . import slave_file
from . import task

parser = cli.parser(
    description="display first lines of a file"
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
    '-n', default=10, type=int,
    help="Number of lines of the file to output."
)

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple files/tasks are being examined"
)

def main():
    cfg, args, m = cli.init(parser)

    for s, t, fobj, show_header in task.files(m, args.task, args.file):
        if not args.q and show_header:
            cli.header(fobj.name())

        for l in itertools.islice(fobj, args.n):
            print l
