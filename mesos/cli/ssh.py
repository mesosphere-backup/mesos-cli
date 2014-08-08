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

import copy
import os
import platform
import sys

import blessings

from .. import cli, log, slave, task
from ..master import current as master

parser = cli.parser(
    description="SSH into the sandbox of a specific task"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task."""
).completer = cli.task_completer

def main():
    term = blessings.Terminal()

    # There's a security bug in Mavericks wrt. urllib2:
    #     http://bugs.python.org/issue20585
    if platform.system() == "Darwin":
        os.environ["no_proxy"] = "*"

    args = cli.init(parser)

    t = master.task(args.task)

    cmd = [
        "ssh",
        "-t",
        t.slave.hostname,
        "cd {0} && bash".format(t.directory)
    ]
    if t.directory == "":
        print term.red + "warning: the task no longer exists on the " + \
            "target slave. Will not enter sandbox" + term.white + "\n\n"
        cmd = cmd[:-1]

    log.fn(os.execvp, "ssh", cmd)
