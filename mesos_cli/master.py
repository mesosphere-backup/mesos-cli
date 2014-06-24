
import itertools
import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading
import logging
import mesos_pb2
import os
import re
import requests
import sys
import urlparse

from . import config
from . import slave
from . import task
from . import util
from . import zookeeper

ZOOKEEPER_TIMEOUT = 1

class MesosMaster(object):

    def __init__(self, cfg):
        self._cfg = cfg.master

    @util.cached_property()
    def host(self):
        return "http://%s" % (self.resolve(self._cfg),)

    def _file_resolver(self, cfg):
        return self.resolve(open(cfg[6:], "r+").read().strip())

    def _zookeeper_resolver(self, cfg):
        hosts, path = cfg[5:].split("/", 1)
        path = "/" + path

        with zookeeper.Client(hosts=hosts, read_only=True) as zk:
            try:
                leader = sorted(
                    [[int(x.split("_")[-1]), x]
                        for x in zk.get_children(path) if re.search("\d+", x)],
                    key=lambda x: x[0])[0][1]
                data, stat = zk.get(os.path.join(path, leader))
            except kazoo.exceptions.NoNodeError:
                logging.error(
                    "%s does not have a valid path. Did you forget /mesos?" % (cfg,))
                sys.exit(1)

            info = mesos_pb2.MasterInfo()
            info.ParseFromString(data)

            return info.pid.split("@")[-1]

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

    @util.cached_property(ttl=30)
    def state(self):
        try:
            return requests.get(urlparse.urljoin(
                self.host, "/master/state.json")).json()
        except requests.exceptions.ConnectionError:
            logging.error("Unable to connect to the master at %s." % (self.host,))
            sys.exit(1)

    @util.memoize
    def slave(self, fltr):
        lst = self.slaves(fltr)

        if len(lst) == 0:
            log.fatal("Cannot find a slave by that name.")

        elif len(lst) > 1:
            result = "There are multiple slaves with that id. Please choose one: "
            for s in lst:
                result += "\n\t{}".format(s.id)
            log.fatal(result)

        return lst[0]

    def slaves(self, fltr):
        return map(lambda x: slave.MesosSlave(x),
            itertools.ifilter(lambda x: fltr in x["id"], self.state["slaves"]))

    def task(self, fltr):
        lst = self.tasks(fltr)

        if len(lst) == 0:
            print "Cannot find a task by that name."
            sys.exit(1)

        elif len(lst) > 1:
            print "There are multiple tasks with that id. Please choose one: "
            for t in lst:
                print "\t{}".format(t.id)
            sys.exit(1)

        return lst[0]

    # XXX - need to filter on task state as well as id
    def tasks(self, fltr=""):
        return map(lambda x: task.Task(self, x),
            itertools.ifilter(lambda x: fltr in x["id"],
                itertools.chain(*[util.merge(x, "tasks", "completed_tasks") for x in
                    self.frameworks])))

    def framework(self, fwid):
        return filter(lambda x: x["id"] == fwid,
            self.frameworks)[0]

    @property
    def frameworks(self):
        return util.merge(current.state, "frameworks", "completed_frameworks")

current = MesosMaster(config.Config())
