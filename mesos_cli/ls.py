
import datetime
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

    Note that this can be a partial match.
""").completer = cli.task_completer

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view.
""")

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple tasks are being examined"
)

def format_line(obj, base):
    human_time = datetime.datetime.fromtimestamp(obj["mtime"]).strftime(
        "%b %d %H:%M")
    fmt = "{mode} {nlink: >3} {uid} {gid} {size: >5} {human_time} {fname}"
    fname = os.path.relpath(obj["path"], base)
    return fmt.format(human_time=human_time, fname=fname, **obj)

def main():
    cfg, args = cli.init(parser)

    tlist = master.tasks(args.task)
    for t in tlist:
        if len(tlist) > 0 and not args.q:
            cli.header(t)

        for f in t.file_list(args.path):
            print format_line(f, os.path.join(t.directory, args.path))
