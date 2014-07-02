
from . import cli

USAGE = """Usage: mesos <command> [OPTIONS]

Available commands:
\t{cmds}
"""

def main():
    print USAGE.format(cmds="\n\t".join(cli.cmds(short=True)))
