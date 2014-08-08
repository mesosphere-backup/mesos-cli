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

import os

import gevent
import gevent.monkey

from .. import cli
from ..master import current as master

gevent.monkey.patch_all()



parser = cli.parser(
    description="observe events from the cluster"
)

parser.add_argument(
    '-s', '--sleep-interval', type=int, default=10,
    help="Sleep approximately N seconds between iterations"
)

parser.add_argument(
    '-q', action='store_true',
    help="Suppresses printing of headers when multiple files/tasks are being examined"
)

last_seen = None

def main():
    args = cli.init(parser)

    active_streams = set()
    jobs = []

    def read_log(log):
        global last_seen
        while True:
            first = True
            for l in log:
                # TODO(thomas) - It is possible for there to be a pause in the
                # middle of this loop (reading the next block from the remote)
                # in this case, the header wouln't be printed and the user would
                # be confused.
                if first and str(log) != last_seen and not args.q:
                    cli.header(log)

                print l

                first = False

            if not first:
                last_seen = str(log)

            gevent.sleep(args.sleep_interval)

    def add_reader(log):
        log.seek(0, os.SEEK_END)
        active_streams.add(log)
        jobs.append(gevent.spawn(read_log, log))

    def find_slaves():
        while True:
            for slave in master.slaves():
                if not slave.log in active_streams:
                    add_reader(slave.log)

            gevent.sleep(args.sleep_interval)

    add_reader(master.log)
    jobs.append(gevent.spawn(find_slaves))
    gevent.joinall(jobs)
