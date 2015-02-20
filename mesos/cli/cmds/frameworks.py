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

from .. import cli
from ..master import CURRENT as MASTER

try:
    from collections import OrderedDict
except ImportError:
    from ordereddict import OrderedDict


parser = cli.parser(
    description="frameworks list"
)

parser.add_argument(
    "-t", "--task-breakdown", action="store_true",
    help="show task status breakdown"
)

parser.add_argument(
    "-i", "--inactive", action="store_true",
    help="show inactive frameworks as well"
)


class TaskStats:
    '''
    To avoid going through the task state for every task state, this class acts as
    a cache that generates the stats for the task in one call and returns it if it
    has been computed already
    '''
    def __init__(self):
        self.stats_cache = dict()

    def get(self, framework_id, tasks, state):
        # check if we have things in the cache already
        if framework_id in self.stats_cache.keys():
            return self._lookup(self.stats_cache[framework_id], state)

        state_count = dict()
        for task in tasks:
            task_state = task['state']
            if task_state in state_count.keys():
                state_count[task_state] += 1
            else:
                state_count[task_state] = 1
        # put the stats in the cache
        self.stats_cache[framework_id] = state_count
        return self._lookup(state_count, state)

    def _lookup(self, state_count, state):
        if state in state_count.keys():
            return state_count[state]
        else:
            return 0


def resource_stats(resource, allocated, used):
    r_used = used[resource]
    r_allocated = allocated[resource]
    if r_allocated > 0:
        percent = int(r_used / r_allocated * 100)
        return str(r_used) + "/" + str(r_allocated) + "(" + str(percent) + "%)"
    else:
        # no resources are being used/allocated
        return "-"

@cli.init(parser)
def main(args):
    term = blessings.Terminal()
    active_task_stats = TaskStats()
    terminal_task_stats = TaskStats()

    table_generator = OrderedDict([
        ("ID", lambda x: x["id"]),
        ("name", lambda x: x["name"]),
        ("host", lambda x: x["hostname"]),
        ("active", lambda x: x["active"]),
        ("cpu", lambda x: resource_stats("cpus", x["resources"], x["used_resources"])),
        ("mem", lambda x: resource_stats("mem", x["resources"], x["used_resources"])),
        ("disk", lambda x: resource_stats("disk", x["resources"], x["used_resources"])),
    ])

    # TODO: the task breakdown is not done in an efficient way (since we traverse the
    # task list on every framework). This can be optimized to do the traversal only
    # once per framework.
    if args.task_breakdown:
        # active tasks
        table_generator['staging'] = lambda x: active_task_stats.get(x["id"], x["tasks"], "TASK_STAGING")
        table_generator['starting'] = lambda x: active_task_stats.get(x["id"], x["tasks"], "TASK_STARTING")
        table_generator['running'] = lambda x: active_task_stats.get(x["id"], x["tasks"], "TASK_RUNNING")
        # terminal state tasks. The count here is approximate since the API caps the result
        # at a max of 1000 tasks
        table_generator['failed'] = lambda x: terminal_task_stats.get(x["id"], x["completed_tasks"], "TASK_FAILED")
        table_generator['killed'] = lambda x: terminal_task_stats.get(x["id"], x["completed_tasks"], "TASK_FAILED")
        table_generator['error'] = lambda x: terminal_task_stats.get(x["id"], x["completed_tasks"], "TASK_ERROR")
        table_generator['lost'] = lambda x: terminal_task_stats.get(x["id"], x["completed_tasks"], "TASK_ERROR")
        table_generator['finished'] = lambda x: terminal_task_stats.get(x["id"], x["completed_tasks"], "TASK_FINISHED")
    else:
        table_generator['active tasks'] = lambda x: len(x["tasks"])

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
        if args.inactive or framework['active']:
            tb.add_row(format_row(framework))
 
    if tb.rowcount == 0:
        print("===>{0}You have no frameworks{1}<===".format(
            term.red, term.white))
    else:
        print(tb)
