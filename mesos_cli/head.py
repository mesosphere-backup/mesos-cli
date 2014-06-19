
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

def main():
    cfg, args, m = cli.init(parser)

    for t in master.tasks(m, args.task):
        s = master.slave(m, t["slave_id"])
        d = task.directory(m, t)
        for f in args.file:
            p = os.path.join(d, f)

            if len(args.task) > 1 or len(args.file):
                print "==> %s:%s/%s <==" % (s["pid"], t["id"], f)

            pos = 0
            for l in slave_file.SlaveFile(s, p).readlines():
                print l

                pos += 1
                if pos >= args.n:
                    break
