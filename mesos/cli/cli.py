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


import argparse
import blessings
import logging
import os

import mesos.cli
from .cfg import current as cfg
from .master import current as master
from . import exceptions
from . import log

def init(parser=None):
    args = parser.parse_args() if parser else None

    logging.basicConfig(
        level=getattr(logging, cfg.log_level.upper()),
        filename=cfg.log_file
    )

    return args

def parser(**kwargs):
    p = argparse.ArgumentParser(
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
    print "==>" + term.red + str(name) + term.white + "<=="

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

    cmds = list(cmds)
    cmds.sort()
    return cmds

def task_completer(prefix, parsed_args, **kwargs):
    return [x.id for x in master.tasks(prefix)]

def slave_completer(prefix, parsed_args, **kwargs):
    return [s.id for s in master.slaves(prefix)]

def file_completer(prefix, parsed_args, **kwargs):
    files = set([])
    split = prefix.rsplit("/", 1)
    base = ""
    if len(split) == 2:
        base = split[0]
    pattern = split[-1]

    for t in master.tasks(parsed_args.task):
        # It is possible for the master to have completed tasks that no longer
        # have files and/or executors
        try:
            for f in t.file_list(base):
                rel = os.path.relpath(f["path"], t.directory)
                if rel.rsplit("/", 1)[-1].startswith(pattern):
                    if f["mode"].startswith("d"):
                        rel += "/"
                    files.add(rel)
        except exceptions.MissingExecutor:
            pass
    return files
