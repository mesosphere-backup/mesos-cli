
import importlib
import os
import sys

from . import cli
from . import log

"""Provide tab completions for python subcommands.

To debug, add `_ARC_DEBUG` to your env.
"""

EXIT = os._exit

def complete_cmd(name=""):
    print "\n".join([x for x in cli.cmds(short=True) if x.startswith(name)])

def cmd_options(cmd):
    os.environ["_ARGCOMPLETE_IFS"] = "\n"
    os.environ["_ARGCOMPLETE_WORDBREAKS"]= os.environ.get("COMP_WORDBREAKS", "")
    os.environ["_ARGCOMPLETE"] = "2"

    try:
        mod = importlib.import_module(
            ".{}".format(cmd), package="mesos_cli")
    except ImportError:
        return
    if not hasattr(mod, 'parser'):
        return
    importlib.import_module("argcomplete").autocomplete(
        mod.parser,
        output_stream=sys.stdout,
        exit_method=EXIT
    )

def main():
    cfg, args = cli.init()

    cmdline = os.environ.get('COMP_LINE') or \
        os.environ.get('COMMAND_LINE') or ''
    cmdpoint = int(os.environ.get('COMP_POINT') or len(cmdline))

    words = cmdline[:cmdpoint].split()

    if len(words) == 1:
        return complete_cmd()
    elif len(words) == 2:
        if cmdline[-1] == " ":
            return cmd_options(words[1])
        else:
            return complete_cmd(words[1])
    else:
        return cmd_options(words[1])
