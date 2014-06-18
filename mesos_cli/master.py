
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

from . import util

ZOOKEEPER_TIMEOUT = 1

def zookeeper_leader(cfg):
    hosts, path = cfg[5:].split("/", 1)
    path = "/" + path

    zk = kazoo.client.KazooClient(hosts=hosts, read_only=True)
    try:
        zk.start(timeout=ZOOKEEPER_TIMEOUT)
    except kazoo.handlers.threading.TimeoutError:
        logging.error("Cannot connect to %s" % (cfg,))
        sys.exit(1)

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

def file_leader(cfg):
    return resolve(open(cfg[6:], "r+").read().strip())

def resolve(cfg):
    """Resolve the URL to the mesos master.

    The value of cfg should be one of:
        - host:port
        - zk://host1:port1,host2:port2/path
        - zk://username:password@host1:port1/path
        - file:///path/to/file (where file contains one of the above)
    """
    if cfg[:3] == "zk:":
        return zookeeper_leader(cfg)
    elif cfg[:5] == "file:":
        return file_leader(cfg)
    else:
        return cfg

def host(cfg):
    return "http://%s" % (resolve(cfg),)

def state(cfg):
    try:
        return requests.get(urlparse.urljoin(
            host(cfg), "/master/state.json")).json()
    except requests.exceptions.ConnectionError:
        logging.error("Unable to connect to the master at %s." % (cfg,))
        sys.exit(1)

def task(state, fltr):
    lst = tasks(state, fltr)

    if len(lst) == 0:
        print "Cannot find a task by that name."
        sys.exit(1)

    elif len(lst) > 1:
        print "There are multiple tasks with that id. Please choose one: "
        for t in lst:
            print "\t" + t["id"]
        sys.exit(1)

    return lst[0]

def tasks(state, fltr=""):
    return filter(lambda x: fltr in x["id"],
        itertools.chain(*[util.merge(x, "tasks", "completed_tasks") for x in
            util.merge(state, "frameworks", "completed_frameworks")]))

def slave(state, i):
    for s in state["slaves"]:
        if s["id"] == i:
            return s
    raise Exception("No slave found")
