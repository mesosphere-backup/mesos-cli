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


import itertools
import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading
import logging
import mesos.interface.mesos_pb2
import os
import re
import requests
import requests.exceptions
import sys
import urlparse

from .cfg import current as cfg
from . import log
from . import mesos_file
from . import slave
from . import task
from . import util
from . import zookeeper

ZOOKEEPER_TIMEOUT = 1

MISSING_MASTER = """unable to connect to a master at {0}.

Try running `mesos config master zk://localhost:2181/mesos`. See the README for
more examples."""

class MesosMaster(object):

    def __str__(self):
        return self.__repr__()

    def __repr__(self):
        return "<master: {0}>".format(self.key())

    def key(self):
        return cfg.master

    @util.cached_property()
    def host(self):
        return "http://%s" % (self.resolve(cfg.master),)

    def fetch(self, url, **kwargs):
        try:
            return requests.get(urlparse.urljoin(
                self.host, url), **kwargs)
        except requests.excption.ConnectionError:
            log.fatal(MISSING_MASTER.format(self.host))

    def _file_resolver(self, cfg):
        return self.resolve(open(cfg[6:], "r+").read().strip())

    def _zookeeper_resolver(self, cfg):
        hosts, path = cfg[5:].split("/", 1)
        path = "/" + path

        with zookeeper.client(hosts=hosts, read_only=True) as zk:
            try:
                leader = sorted(
                    [[int(x.split("_")[-1]), x]
                        for x in zk.get_children(path) if re.search("\d+", x)],
                    key=lambda x: x[0])

                if len(leader) == 0:
                    log.fatal("cannot find any masters at {0}".format(cfg,))
                data, stat = zk.get(os.path.join(path, leader[0][1]))
            except kazoo.exceptions.NoNodeError:
                log.fatal(
                    "{0} does not have a valid path. Did you forget /mesos?".format(cfg))

            # Old versions of mesos stick a PID into zookeeper instead of the
            # current MasterInfo. If the protobuf can't be decoded for whatever
            # reason, assume that it is the old method.
            val = None
            try:
                info = mesos.interface.mesos_pb2.MasterInfo()
                info.ParseFromString(data)
                val = info.pid
            except google.protobuf.message.DecodeError:
                val = data

            return val.split("@")[-1]

    def resolve(self, cfg):
        """Resolve the URL to the mesos master.

        The value of cfg should be one of:
            - host:port
            - zk://host1:port1,host2:port2/path
            - zk://username:password@host1:port1/path
            - file:///path/to/file (where file contains one of the above)
        """
        if cfg[:3] == "zk:":
            return self._zookeeper_resolver(cfg)
        elif cfg[:5] == "file:":
            return self._file_resolver(cfg)
        else:
            return cfg

    @util.cached_property(ttl=5)
    def state(self):
        return self.fetch("/master/state.json").json()

    @util.memoize
    def slave(self, fltr):
        lst = self.slaves(fltr)

        if len(lst) == 0:
            log.fatal("Cannot find a slave by that name.")

        elif len(lst) > 1:
            result = "There are multiple slaves with that id. Please choose one: "
            for s in lst:
                result += "\n\t{0}".format(s.id)
            log.fatal(result)

        return lst[0]

    def slaves(self, fltr=""):
        return map(lambda x: slave.MesosSlave(x),
            itertools.ifilter(lambda x: fltr in x["id"], self.state["slaves"]))

    def task(self, fltr):
        lst = self.tasks(fltr)

        if len(lst) == 0:
            log.fatal("Cannot find a task by that name.")

        elif len(lst) > 1:
            msg = ["There are multiple tasks with that id. Please choose one:"]
            msg += ["\t{0}".format(t.id) for t in lst]
            log.fatal("\n".join(msg))

        return lst[0]

    # XXX - need to filter on task state as well as id
    def tasks(self, fltr="", active_only=False):
        keys = [ "tasks" ]
        if not active_only:
            keys.append("completed_tasks")
        return map(lambda x: task.Task(self, x),
            itertools.ifilter(lambda x: fltr in x["id"],
                itertools.chain(*[util.merge(x, *keys) for x in
                    self.frameworks(active_only)])))

    def framework(self, fwid):
        return filter(lambda x: x["id"] == fwid,
            self.frameworks())[0]

    def frameworks(self, active_only=False):
        keys = [ "frameworks" ]
        if not active_only:
            keys.append("completed_frameworks")
        return util.merge(self.state, *keys)

    @property
    @util.memoize
    def log(self):
        return mesos_file.File(self, path="/master/log")

current = MesosMaster()
