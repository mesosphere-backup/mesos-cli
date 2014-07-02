
import argcomplete
import json

from . import cli
from .master import current as master

parser = cli.parser(
    description="fetch the json state for either the master or a specific slave"
)

parser.add_argument(
    "slave", nargs="?",
    help="ID of the slave. May match multiple slaves (or all)"
).completer = cli.slave_completer

def main():
    cfg, args = cli.init(parser)

    if not args.slave:
        print json.dumps(master.state, indent=4)
    else:
        print json.dumps([s.state for s in master.slaves(args.slave)], indent=4)
