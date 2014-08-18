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

import os
import sys

from . import cli, log


FAILURE_MESSAGE = """'{}' is not a valid command (or cannot be found)

To see a list of commands, run `mesos help`."""


def main():
    if len(sys.argv) == 1:
        cmd = "mesos-help"
    else:
        cmd = "mesos-" + sys.argv[1]

    if cmd in cli.cmds():
        log.fn(os.execvp, cmd, [cmd] + sys.argv[2:])
    else:
        log.fatal(FAILURE_MESSAGE.format(cmd))
