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

import prettytable

import blessings

from .. import cli, util
from ..master import CURRENT as MASTER

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


parser = cli.parser(
    description="process status"
)

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive tasks as well"
)


def get_memory(x):
    max_mem = x["resources"]["mem"] * 1024 * 1024 * 1.0
    return "{0:.2f}".format((x.rss / max_mem) * 100)


@cli.handle_signals
def main():
    term = blessings.Terminal()

    table_generator = OrderedDict([
        # user_time + system_time
        ("time", lambda x: x.cpu_time),
        ("state", lambda x: x["state"].split("_")[-1][0]),
        # mem_rss
        ("rss", lambda x: util.humanize_bytes(x.rss)),
        # cpus_limit
        ("cpu", lambda x: x.cpu_limit),
        # mem_rss / mem_limit
        ("%mem", get_memory),
        # executor.name
        ("command", lambda x: x.command),
        ("user", lambda x: x.user),
        # task_id
        ("id", lambda x: x["id"]),
    ])

    args = cli.init(parser)

    tb = prettytable.PrettyTable(
        [x.upper() for x in table_generator.keys()],
        border=False,
        max_table_width=term.width,
        hrules=prettytable.NONE,
        vrules=prettytable.NONE,
        left_padding_width=0,
        right_padding_width=1
    )

    for task in MASTER.tasks(active_only=(not args.inactive)):
        tb.add_row([fn(task) for fn in table_generator.values()])

    if tb.rowcount == 0:
        print("===>{0}You have no tasks for that filter{1}<===".format(
            term.red, term.white))
    else:
        print(tb)
