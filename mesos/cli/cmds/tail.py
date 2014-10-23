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

import functools
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
    "-i", "--inactive", action="store_true",
    help="show inactive tasks as well"
)

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


def until_end(fobj):
    global files_seen

    fobj.seek(files_seen.get(fobj, 0))
    return list(fobj)


def read_file(fn, fobj):
    global files_seen

    lines = fn(fobj)
    files_seen[fobj] = fobj.tell()

    return (str(fobj), lines)


@cli.init(parser)
def main(args):

    def last_lines(fobj):
        return reversed(list(itertools.islice(reversed(fobj), args.n)))

    def output(fn):
        for (fname, lines) in cluster.files(
                functools.partial(read_file, fn),
                args.task,
                args.file,
                active_only=not args.inactive,
                fail=(not args.follow)):
            cli.output_file(
                lines, not args.q, key=fname)

    output(last_lines)

    if args.follow:
        while True:
            output(until_end)
            time.sleep(RECHECK)
