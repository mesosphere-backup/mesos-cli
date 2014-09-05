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

import contextlib
import itertools

import concurrent.futures

from .cfg import CURRENT as CFG


@contextlib.contextmanager
def execute():
    with concurrent.futures.ThreadPoolExecutor(
            max_workers=CFG["max_workers"]) as executor:
        yield executor


def by_fn(keyfn, fn, items):
    """Call fn in parallel across items based on keyfn.

    Extensive caching/memoization is utilized when fetching data.
    When you run a function against tasks in a completely parallel way, the
    caching is skipped and there is the possibility that your endpoint will
    receive multiple requests. For most use cases, this significantly slows
    the result down (instead of speeding it up).

    The solution to this predicament is to execute fn in parallel but only
    across a specific partition function (slave ids in this example).
    """
    jobs = []

    with execute() as executor:

        # itertools.groupby returns a list of (key, generator) tuples. A job
        # is submitted and then the local execution context continues. The
        # partitioned generator is destroyed and you only end up executing fn
        # over a small subset of the desired partition. Therefore, the list()
        # conversion when submitting the partition for execution is very
        # important.
        for k, part in itertools.groupby(items, keyfn):
            jobs.append(executor.submit(lambda: [fn(i) for i in list(part)]))

    for job in concurrent.futures.as_completed(jobs):
        for result in job.result():
            yield result


def by_slave(fn, tasks):
    """Execute a function against tasks partitioned by slave."""

    keyfn = lambda x: x.slave["id"]
    tasks = sorted(tasks, key=keyfn)
    return by_fn(keyfn, fn, tasks)
