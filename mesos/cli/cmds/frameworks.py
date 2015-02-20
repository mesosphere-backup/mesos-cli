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

import blessings
import prettytable

from .. import cli, exceptions, parallel, util
from ..master import CURRENT as MASTER

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


parser = cli.parser(
    description="frameworks list"
)

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive frameworks as well"
)

@cli.init(parser)
def main(args):
    term = blessings.Terminal()
    
    #print(args.inactive)

    table_generator = OrderedDict([
        ("ID", lambda x: x["id"]),
        ("name", lambda x: x["name"]),
    ])

    tb = prettytable.PrettyTable(
        [x.upper() for x in table_generator.keys()],
        border=False,
        max_table_width=term.width,
        hrules=prettytable.NONE,
        vrules=prettytable.NONE,
        left_padding_width=0,
        right_padding_width=1
    )

    def format_row(framework):
        return [fn(framework) for fn in table_generator.values()]

    for framework in MASTER.state['frameworks']:
        tb.add_row(format_row(framework))

    if tb.rowcount == 0:
        print("===>{0}You have no frameworks{1}<===".format(
            term.red, term.white))
    else:
        print(tb)
