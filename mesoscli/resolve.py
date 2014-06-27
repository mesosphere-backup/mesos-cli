
from . import cli
from . import config
from .master import current as master

parser = cli.parser(
    description="return the host/port for the currently leading master."
)

parser.add_argument(
    "master", nargs="?", default=config.Config().master
)

def main():
    cfg, args = cli.init(parser)

    print master.resolve(args.master)
