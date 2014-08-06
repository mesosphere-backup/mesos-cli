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


import functools
import itertools
import os
import time

from .. import cli
from ..master import current as master
from .. import task

RECHECK = 1

parser = cli.parser(
    description="display the last part of a file"
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
    '-f', '--follow', action='store_true',
    help="Wait for additional data to be appended to the file."
)

parser.add_argument(
    '-n', default=10, type=int,
    help="Number of lines of the file to tail."
)

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple files/tasks are being examined"
)

files_seen = {}
last_seen = None

def follow(args):
    global last_seen
    for s, t, fobj, show_header in task.files(args.task, args.file, fail=False):

        fobj.seek(files_seen.get(fobj, 0))
        first = True

        for l in fobj:
            if first and str(log) != last_seen and not args.q:
                cli.header(fobj)

            print l

            first = False

        files_seen[fobj] = fobj.tell()

        if not first:
            last_seen = fobj

def main():
    global last_seen
    args = cli.init(parser)

    for s, t, fobj, show_header in task.files(args.task, args.file,
            fail=(not args.follow)):
        if not args.q and show_header:
            cli.header(fobj,)

        lines = list(itertools.islice(reversed(fobj), args.n))
        for l in reversed(lines):
            print l

        files_seen[fobj] = fobj.last_size
        last_seen = fobj

    if args.follow:
        while 1:
            follow(args)
            time.sleep(RECHECK)
