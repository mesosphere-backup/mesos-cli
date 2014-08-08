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


import itertools
import os

from .. import cli, task
from ..master import current as master

parser = cli.parser(
    description="display first lines of a file"
)

parser.add_argument(
    'task',
    help="ID of the task. May match multiple tasks (or all)"
).completer = cli.task_completer

parser.add_argument(
    'file', nargs="*", default=["stdout"],
    help="Path to the file inside the task's sandbox."
).completer = cli.file_completer

parser.add_argument(
    '-n', default=10, type=int,
    help="Number of lines of the file to output."
)

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple files/tasks are being examined"
)

def main():
    args = cli.init(parser)

    for s, t, fobj, show_header in task.files(args.task, args.file):
        if not args.q and show_header:
            cli.header(fobj)

        for l in itertools.islice(fobj, args.n):
            print l
