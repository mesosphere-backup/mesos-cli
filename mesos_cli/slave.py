
import itertools
import logging
import requests
import sys
import urlparse

from . import log
from . import util

class MesosSlave(object):

    def __init__(self, meta):
        self._meta = meta

    def __getattr__(self, name):
        if name in self._meta:
            return self._meta[name]
        raise AttributeError()

    @property
    def host(self):
        return "http://{}:{}".format(
            self.hostname,
            self.pid.split(":")[-1])

    def fetch(self, url, **kwargs):
        try:
            return requests.get(urlparse.urljoin(
                self.host, url), **kwargs)
        except requests.excption.ConnectionError:
            log.fatal("Unable to connect to the slave at {}.".format(self.host))

    @util.cached_property()
    def state(self):
        return self.fetch("/slave(1)/state.json").json()

    @property
    def frameworks(self):
        return util.merge(self.state, "frameworks", "completed_frameworks")

    def task_executor(self, task_id):
        for fw in self.frameworks:
            for exc in util.merge(fw, "executors", "completed_executors"):
                if task_id in map(lambda x: x["id"], exc["tasks"]):
                    return exc
        raise Exception("No executor has a task by that id")

    def file_list(self, path):
        resp = self.fetch("/files/browse.json", params={ "path": path })
        if resp.status_code == 404:
            return []
        return resp.json()

    def file(self, task, path):
        return slave_file.SlaveFile(self, task, path)

    @util.cached_property(ttl=1)
    def stats(self):
        return self.fetch("/monitor/statistics.json").json()

    def executor_stats(self, _id):
        return filter(lambda x: x["executor_id"])

    def task_stats(self, _id):
        eid = self.task_executor(_id)["id"]
        return filter(lambda x: x["executor_id"] == eid,
            self.stats)[0]["statistics"]
