
import os

from . import cli
from . import master
from . import slave
from . import task

parser = cli.parser(
    description="List all the files inside a specific task's sandbox"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task.

    Note that this can be a partial match."""
)

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view."""
)

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple tasks are being examined"
)

def main():
    cfg, args, m = cli.init(parser)

    tlist = master.tasks(m, args.task)
    for t in tlist:
        s = master.slave(m, t["slave_id"])
        base = os.path.join(task.directory(m, t), args.path)

        def walk_dir(flist, pth):
            for f in flist:
                print os.path.relpath(f["path"], base)
                if f["mode"][0] == "d":
                    walk_dir(slave.file_list(s, f["path"]), f["path"])

        flist = slave.file_list(s, base)
        if len(flist) > 0:
            if len(tlist) > 0 and not args.q:
                cli.header("%s:%s" % (s["pid"], t["id"]))
            walk_dir(flist, base)

