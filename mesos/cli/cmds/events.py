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

import os
import time

import concurrent.futures

from .. import cli
from ..master import CURRENT as MASTER

parser = cli.parser(
    description="observe events from the cluster"
)

parser.add_argument(
    '-s', '--sleep-interval', type=float, default=5,
    help="Sleep approximately N seconds between iterations"
)

parser.enable_print_header()

# Testing helpers
FOLLOW = True
POSITION = os.SEEK_END


# TODO(thomasr) - Should operate identical to tail, output the last couple
# lines before beginning to follow.
@cli.handle_signals
def main():
    args = cli.init(parser)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        active_streams = set()
        jobs = set()

        def read_log(log, sleep=args.sleep_interval):
            time.sleep(sleep)
            cli.output_file(log, args.q)
            return log

        def add_reader(log):
            log.seek(0, POSITION)
            active_streams.add(log)
            jobs.add(executor.submit(read_log, log, 0))

        def find_slaves():
            for slave in MASTER.slaves():
                if slave.log not in active_streams:
                    add_reader(slave.log)

        add_reader(MASTER.log)
        while True:
            done, jobs = concurrent.futures.wait(
                jobs, return_when=concurrent.futures.FIRST_COMPLETED)
            for job in done:
                jobs.add(executor.submit(read_log, job.result()))
            find_slaves()

            if not FOLLOW:
                break
