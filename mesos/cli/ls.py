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


import datetime
import os

from . import cli
from .master import current as master
from . import slave
from . import task

parser = cli.parser(
    description="List all the files inside a specific task's sandbox"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task.

    Note that this can be a partial match.
""").completer = cli.task_completer

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view.
""").completer = cli.file_completer

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple tasks are being examined"
)

def format_line(obj, base):
    human_time = datetime.datetime.fromtimestamp(obj["mtime"]).strftime(
        "%b %d %H:%M")
    fmt = "{mode} {nlink: >3} {uid} {gid} {size: >5} {human_time} {fname}"
    fname = os.path.relpath(obj["path"], base)
    return fmt.format(human_time=human_time, fname=fname, **obj)

def main():
    args = cli.init(parser)

    tlist = master.tasks(args.task)
    for t in tlist:
        if len(tlist) > 1 and not args.q:
            cli.header(t)

        p = args.path
        if p.endswith("/"):
            p = p[:-1]
        for f in t.file_list(p):
            print format_line(f, os.path.join(t.directory, args.path))
