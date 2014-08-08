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

from .. import cli, completion_helpers
from ..master import CURRENT as MASTER

parser = cli.parser(
    description="List all the files inside a specific task's sandbox"
)

parser.add_argument(
    'task', type=str,
    help="""Name of the task.

    Note that this can be a partial match."""
).completer = completion_helpers.task

parser.add_argument(
    'path', type=str, nargs="?", default="",
    help="""Path to view."""
).completer = completion_helpers.file

parser.enable_print_header()


@cli.handle_signals
def main():
    args = cli.init(parser)

    tlist = MASTER.tasks(args.task)
    path = args.path
    if path.endswith("/"):
        path = path[:-1]

    for task in tlist:
        base = os.path.join(task.directory, path)
        flist = task.file_list(path)

        def walk_dir(flist):
            for file_meta in flist:
                print(os.path.relpath(file_meta["path"], base))
                if file_meta["mode"][0].startswith("d"):
                    walk_dir(task.file_list(file_meta["path"]))

        if len(tlist) > 1 and not args.q:
            cli.header(task)
        if len(flist) > 0:
            walk_dir(flist)
