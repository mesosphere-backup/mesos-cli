
from . import cli

USAGE = """Usage: mesos <command> [OPTIONS]

Available commands:
\t{cmds}
"""

def main():
    cmds = [x.split("-")[-1] for x in cli.cmds()]

    print USAGE.format(cmds="\n\t".join(cmds))
