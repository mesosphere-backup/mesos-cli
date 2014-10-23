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

from .. import cli, cluster

parser = cli.parser(
    description="display first lines of a file"
)

parser.task_argument()
parser.file_argument()

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive tasks as well"
)

parser.add_argument(
    '-n', default=10, type=int,
    help="Number of lines of the file to output."
)

parser.enable_print_header()


@cli.init(parser)
def main(args):

    def read_file(fobj):
        return (str(fobj), list(itertools.islice(fobj, args.n)))

    for (fname, lines) in cluster.files(
            read_file,
            args.task,
            args.file,
            active_only=not args.inactive):
        cli.output_file(lines, not args.q, key=fname)
