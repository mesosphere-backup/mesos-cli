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


import datetime
import os
import re
import urlparse

import requests

from . import exceptions, log, mesos_file, slave, util


class Task(dict):

    cmd_re = re.compile("\(Command: (.+)\)")

    def __init__(self, master, meta):
        self.master = master
        self._meta = meta

    def __str__(self):
        return "{0}:{1}".format(
            self.slave.pid.split('@')[-1].split(':')[0], self.id)

    def __repr__(self):
        return self.__str__()

    def __getattr__(self, name):
        if name in self._meta:
            return self._meta[name]
        raise AttributeError()

    @property
    def executor(self):
        return self.slave.task_executor(self.id)

    @property
    def framework(self):
        # Preventing circular imports
        from .master import current as master
        return master.framework(self.framework_id)

    @util.cached_property()
    def directory(self):
        try:
            return self.executor["directory"]
        except exceptions.MissingExecutor:
            return ""

    @util.cached_property()
    def slave(self):
        return self.master.slave(self._meta["slave_id"])

    def file(self, path):
        return mesos_file.File(self.slave, self, path)

    def file_list(self, path):
        return self.slave.file_list(os.path.join(self.directory, path))

    @property
    def stats(self):
        try:
            return self.slave.task_stats(self.id)
        except exceptions.MissingExecutor:
            return {}

    @property
    def cpu_time(self):
        st = self.stats
        secs = st.get("cpus_user_time_secs", 0) + \
            st.get("cpus_system_time_secs", 0)
        # timedelta has a resolution of .000000 while mesos only keeps .00
        return str(datetime.timedelta(seconds=secs))[:-4]

    @property
    def cpu_limit(self):
        return self.stats.get("cpus_limit", 0)

    @property
    def mem_limit(self):
        return self.stats.get("mem_limit_bytes", 0)

    @property
    def rss(self):
        return self.stats.get("mem_rss_bytes", 0)

    @property
    def command(self):
        try:
            result = self.cmd_re.search(self.executor["name"])
        except exceptions.MissingExecutor:
            result = None
        if not result:
            return "none"
        return result.group(1)

    @property
    def user(self):
        return self.framework["user"]

def files(fltr, flist, fail=True):
    # Preventing circular imports
    from .master import current as master

    tlist = master.tasks(fltr)
    mult = len(tlist) > 1 or len(flist) > 1
    dne = True

    for t in tlist:
        for f in flist:
            fobj = t.file(f)
            if fobj.exists():
                dne = False
                yield (t.slave, t, fobj, mult)

    if dne and fail:
        log.fatal("No such task has the requested file or directory")
