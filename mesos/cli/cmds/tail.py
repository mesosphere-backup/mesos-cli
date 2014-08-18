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

from .. import cli, cluster

RECHECK = 1

parser = cli.parser(
    description="display the last part of a file"
)

parser.task_argument()
parser.file_argument()

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


@cli.handle_signals
def main():
    global files_seen
    args = cli.init(parser)

    for fobj, show_header in cluster.files(
            args.task, args.file, fail=(not args.follow)):
        if not args.q and show_header:
            cli.header(fobj,)

        lines = list(itertools.islice(reversed(fobj), args.n))
        for line in reversed(lines):
            print(line)

        files_seen[fobj] = fobj.tell()
        if len(lines) > 0:
            cli.last_seen = str(fobj)

    def follow():
        global files_seen
        for fobj, show_header in cluster.files(
                args.task, args.file, fail=False):

            fobj.seek(files_seen.get(fobj, 0))
            cli.output_file(fobj, args.q)
            files_seen[fobj] = fobj.tell()

    if args.follow:
        while True:
            follow()
            time.sleep(RECHECK)
