
import datetime
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

    Note that this can be a partial match.
""")

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view.
""")

def format_line(obj, base):
    human_time = datetime.datetime.fromtimestamp(obj["mtime"]).strftime(
        "%b %d %H:%M")
    fmt = "{mode} {nlink: >3} {uid} {gid} {size: >5} {human_time} {fname}"
    fname = os.path.relpath(obj["path"], base)
    return fmt.format(human_time=human_time, fname=fname, **obj)

def main():
    cfg, args, m = cli.init(parser)

    for t in master.tasks(m, args.task):
        d = os.path.join(task.directory(m, t), args.path)

        flist = slave.file_list(master.slave(m, t["slave_id"]), d)
        if len(flist) > 0:
            print '--%s' % (t["id"],)

        for f in flist:
            print format_line(f, d)
