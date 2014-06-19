
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

    tlist = master.tasks(m, args.task)
    for t in tlist:
        s = master.slave(m, t["slave_id"])
        d = task.directory(m, t)
        for f in args.file:
            p = os.path.join(d, f)

            if not args.q and (len(tlist) > 1 or len(args.file) > 1):
                cli.file_header(s, t, f)

            for l in itertools.islice(
                    slave_file.SlaveFile(s, p).readlines(), args.n):
                print l
