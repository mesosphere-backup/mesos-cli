
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
""")

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
        s = master.slave(t["slave_id"])
        d = os.path.join(task.directory(t), args.path)

        flist = slave.file_list(s, d)
        if len(tlist) > 0 and not args.q:
            cli.header("%s:%s" % (s["pid"], t["id"]))

        for f in flist:
            print format_line(f, d)
