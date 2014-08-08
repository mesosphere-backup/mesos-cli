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

import concurrent.futures
import itertools
import os

from .. import cli, log
from ..master import CURRENT as MASTER

parser = cli.parser(
    description="upload the specified local file(s) to all slaves"
)

parser.add_argument(
    "file", nargs="+",
    help="Local files to upload to the slaves"
)

parser.add_argument(
    "remote_path",
    help="Remote path to upload local files to"
)


def upload(slave, src, dst):
    cmd = [
        "scp",
        "-pr",
        src,
        "{0}:{1}".format(slave["hostname"], dst)
    ]
    try:
        return (slave, src, dst, log.fn(gevent.subprocess.check_call, cmd))
    except gevent.subprocess.CalledProcessError, e:
        return (slave, e.returncode)


def main():
    args = cli.init(parser)

    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as executor:
        for slave in MASTER.slaves():
            for fname in args.file:
                executor.submit(upload, slave, fname, args.remote_path)

        for

    # jobs = list(itertools.chain(
    #     *[[gevent.spawn(upload, s, f, args.remote_path) for f in args.file]
    #         for s in MASTER.slaves()]))

    # gevent.joinall(jobs)

    # for slave, src, dst, retcode in [x.value for x in jobs]:
    #     print("{0}:{1}\t{2}".format(
    #         slave["hostname"], os.path.join(dst, src),
    #         "uploaded" if retcode == 0 else "failed"))
