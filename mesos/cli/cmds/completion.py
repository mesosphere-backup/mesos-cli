# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


from __future__ import absolute_import, print_function

import importlib
import os
import sys

from .. import cli

"""Provide tab completions for python subcommands.

To debug, add `_ARC_DEBUG` to your env.
"""

EXIT = sys.exit


def complete_cmd(name=""):
    print("\n".join([x for x in cli.cmds(short=True) if x.startswith(name)]))


def cmd_options(cmd):
    os.environ["_ARGCOMPLETE_IFS"] = "\n"
    os.environ["_ARGCOMPLETE_WORDBREAKS"] = os.environ.get(
        "COMP_WORDBREAKS", "")
    os.environ["_ARGCOMPLETE"] = "2"

    try:
        mod = importlib.import_module(
            ".{0}".format(cmd), package="mesos.cli.cmds")
    except ImportError:
        return

    if not hasattr(mod, 'parser'):
        return

    importlib.import_module("argcomplete").autocomplete(
        mod.parser,
        output_stream=sys.stdout,
        exit_method=EXIT
    )


def usage():
    print("""Please look at the README for instructions on setting command
completion up for your shell.""")


@cli.init
def main(args):
    cmdline = os.environ.get('COMP_LINE') or \
        os.environ.get('COMMAND_LINE') or ''
    cmdpoint = int(os.environ.get('COMP_POINT') or len(cmdline))

    words = cmdline[:cmdpoint].split()

    if len(words) == 0:
        return usage()
    elif len(words) == 1:
        return complete_cmd()
    elif len(words) == 2:
        if cmdline[-1] == " ":
            return cmd_options(words[1])
        else:
            return complete_cmd(words[1])
    else:
        return cmd_options(words[1])
