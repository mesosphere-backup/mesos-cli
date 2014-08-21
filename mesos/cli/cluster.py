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

from . import cli, exceptions, log
from .master import CURRENT as MASTER

missing_slave = set([])


def files(fltr, flist, fail=True):
    tlist = MASTER.tasks(fltr)
    mult = len(tlist) > 1 or len(flist) > 1
    dne = True

    for task in tlist:
        for fname in flist:

            try:
                fobj = task.file(fname)
            except exceptions.SlaveDoesNotExist:
                if task["id"] not in missing_slave:
                    cli.header("{0}:{1}".format(
                        task["id"], fname))
                    print("Slave no longer exists.")

                missing_slave.add(task["id"])
                break

            if fobj.exists():
                dne = False
                yield (fobj, mult)

    if dne and fail:
        log.fatal("No such task has the requested file or directory")
