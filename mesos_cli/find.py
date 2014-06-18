
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

def main():
    cfg, args, m = cli.init(parser)

    for t in master.tasks(m, args.task):
        s = master.slave(m, t["slave_id"])
        base = os.path.join(task.directory(m, t), args.path)

        def walk_dir(flist, pth):
            for f in flist:
                print os.path.relpath(f["path"], base)
                if f["mode"][0] == "d":
                    walk_dir(slave.files(s, f["path"]), f["path"])

        flist = slave.files(s, base)
        if len(flist) > 0:
            print "--%s" % (t["id"],)
            walk_dir(flist, base)

