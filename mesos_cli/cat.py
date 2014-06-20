
import os
import sys

from . import cli
from .master import current as master
from . import slave
from . import slave_file
from . import task

parser = cli.parser(
    description="concatenate and print files"
)

parser.add_argument(
    'task',
    help="ID of the task. May match multiple tasks (or all)"
)

parser.add_argument(
    'file', type=str, nargs="*", default=["stdout"],
    help="Path to the file inside the task's sandbox."
)

def main():
    cfg, args = cli.init(parser)

    for t in master.tasks(args.task):
        for f in args.file:
            for l in t.file(f):
                print l
