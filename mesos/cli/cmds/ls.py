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

import datetime
import os

from .. import cli, exceptions
from ..master import CURRENT as MASTER

parser = cli.parser(
    description="List all the files inside a specific task's sandbox"
)

parser.task_argument()
parser.path_argument()
parser.enable_print_header()


def format_line(obj, base):
    human_time = datetime.datetime.fromtimestamp(obj["mtime"]).strftime(
        "%b %d %H:%M")
    fmt = "{mode} {nlink: >3} {uid} {gid} {size: >5} {human_time} {fname}"
    fname = os.path.relpath(obj["path"], base)
    return fmt.format(human_time=human_time, fname=fname, **obj)


@cli.init(parser)
def main(args):
    tlist = MASTER.tasks(args.task)
    for task in tlist:
        if len(tlist) > 1 and not args.q:
            cli.header(task)

        p = args.path
        if p.endswith("/"):
            p = p[:-1]

        try:
            for fobj in task.file_list(p):
                print(format_line(
                    fobj, os.path.join(task.directory, args.path)))
        except exceptions.SlaveDoesNotExist:
            continue
