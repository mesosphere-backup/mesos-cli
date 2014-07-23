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


import blessings
import collections
import prettytable
import util

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict

from . import cli
from .master import current as master

parser = cli.parser(
    description="process status"
)

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive tasks as well"
)

def get_memory(x):
    if x.mem_limit == 0:
        return "0"
    else:
        return "{0:.2f}".format((x.rss / (x.mem_limit * 1.0)) * 100)

def main():
    term = blessings.Terminal()
    max_pid = term.width - 70

    table_generator = OrderedDict([
        # user_time + system_time
        ("time", lambda x: x.cpu_time),
        # mem_rss
        ("rss", lambda x: util.humanize_bytes(x.rss)),
        # cpus_limit
        ("cpu", lambda x: x.cpu_limit),
        # mem_rss / mem_limit
        ("%mem", get_memory),
        # executor.name
        ("command", lambda x: x.command),
        ("user", lambda x: x.user),
        # slave_pid:task_id
        ("pid", lambda x: str(x).split('@')[-1][:max_pid]),
    ])

    cfg, args = cli.init(parser)

    tb = prettytable.PrettyTable(
        [x.upper() for x in table_generator.keys()],
        border=False,
        max_table_width=term.width,
        hrules=prettytable.NONE,
        vrules=prettytable.NONE,
        left_padding_width=0,
        right_padding_width=1
    )

    for t in master.tasks(active_only=(not args.inactive)):
        tb.add_row([fn(t) for fn in table_generator.values()])
    print tb
