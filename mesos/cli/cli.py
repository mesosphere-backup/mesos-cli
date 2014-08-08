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

import argparse
import logging
import os

import blessings
import mesos.cli

from .cfg import CURRENT as CFG


class ArgumentParser(argparse.ArgumentParser):

    def enable_print_header(self):
        self.add_argument(
            '-q', action='store_true',
            help="Suppresses printing of headers when multiple tasks are " +
                 "being examined"
        )


def init(parser=None):
    args = parser.parse_args() if parser else None

    logging.basicConfig(
        level=getattr(logging, CFG["log_level"].upper()),
        filename=CFG["log_file"]
    )

    return args


def parser(**kwargs):
    p = ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        **kwargs
    )

    p.add_argument(
        "-v", "--version",
        action="version", version="%(prog)s {0}".format(mesos.cli.__version__)
    )
    return p


def header(name):
    term = blessings.Terminal()
    print("==>" + term.red + str(name) + term.white + "<==")


def cmds(short=False):
    def fltr(cmd):
        if not cmd.startswith("mesos-"):
            return False
        if cmd.endswith(".sh"):
            return False
        return True

    cmds = set([])
    for path in os.environ.get("PATH").split(os.pathsep):
        try:
            cmds = cmds.union(filter(fltr, os.listdir(path)))
        except OSError:
            pass

    if short:
        cmds = [x.split("-", 1)[-1] for x in cmds]

    return sorted(cmds)
