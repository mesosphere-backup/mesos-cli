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

    Note that this can be a partial match."""
).completer = cli.task_completer

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view."""
).completer = cli.file_completer

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple tasks are being examined"
)

def main():
    args = cli.init(parser)

    tlist = master.tasks(args.task)
    path = args.path
    if path.endswith("/"):
        path = path[:-1]

    for t in tlist:
        base = os.path.join(t.directory, path)
        flist = t.file_list(path)

        def walk_dir(flist):
            for f in flist:
                print os.path.relpath(f["path"], base)
                if f["mode"][0].startswith("d"):
                    walk_dir(t.file_list(f["path"]))

        if len(tlist) > 1 and not args.q:
            cli.header(t)
        if len(flist) > 0:
            walk_dir(flist)
