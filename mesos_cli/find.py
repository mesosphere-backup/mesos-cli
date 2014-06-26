
import os

from . import cli
from .master import current as master
from . import slave
from . import task

parser = cli.parser(
    description="List all the files inside a specific task's sandbox"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task.

    Note that this can be a partial match."""
).completer = cli.task_completer

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view."""
).completer = cli.file_completer

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple tasks are being examined"
)

def main():
    cfg, args = cli.init(parser)

    tlist = master.tasks(args.task)
    path = args.path
    if path.endswith("/"):
        path = path[:-1]

    for t in tlist:
        base = os.path.join(t.directory, path)
        flist = t.file_list(path)

        def walk_dir(flist):
            for f in flist:
                print os.path.relpath(f["path"], base)
                if f["mode"][0].startswith("d"):
                    walk_dir(t.file_list(f["path"]))

        if len(tlist) > 1 and not args.q:
            cli.header(t)
        if len(flist) > 0:
            walk_dir(flist)
