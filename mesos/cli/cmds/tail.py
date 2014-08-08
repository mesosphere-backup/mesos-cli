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

import itertools
import time

from .. import cli, cluster, completion_helpers

RECHECK = 1

parser = cli.parser(
    description="display the last part of a file"
)

parser.add_argument(
    'task',
    help="ID of the task. May match multiple tasks (or all)"
).completer = completion_helpers.task

parser.add_argument(
    'file', nargs="*", default=["stdout"],
    help="Path to the file inside the task's sandbox."
).completer = completion_helpers.file

parser.add_argument(
    '-f', '--follow', action='store_true',
    help="Wait for additional data to be appended to the file."
)

parser.add_argument(
    '-n', default=10, type=int,
    help="Number of lines of the file to tail."
)

parser.enable_print_header()

files_seen = {}
last_seen = None


def follow(args):
    global files_seen, last_seen
    for fobj, show_header in cluster.files(args.task, args.file, fail=False):

        fobj.seek(files_seen.get(fobj, 0))
        first = True

        for line in fobj:
            if first and str(fobj) != last_seen and not args.q:
                cli.header(fobj)

            print(line)

            first = False

        files_seen[fobj] = fobj.tell()

        if not first:
            last_seen = str(fobj)


def main():
    global files_seen, last_seen
    args = cli.init(parser)

    for fobj, show_header in cluster.files(
            args.task, args.file, fail=(not args.follow)):
        if not args.q and show_header:
            cli.header(fobj,)

        lines = list(itertools.islice(reversed(fobj), args.n))
        for line in reversed(lines):
            print(line)

        files_seen[fobj] = fobj.tell()
        last_seen = str(fobj)

    if args.follow:
        while 1:
            follow(args)
            time.sleep(RECHECK)
