
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

    def executor(self, fltr):
        for fw in self.state["frameworks"]:
            for exc in util.merge(fw, "executors", "completed_executors"):
                if fltr in exc["id"]:
                    return exc
        raise Exception("No executor by that id")

    def file_list(self, path):
        resp = self.fetch("/files/browse.json", params={ "path": path })
        if resp.status_code == 404:
            return []
        return resp.json()

    def file(self, task, path):
        return slave_file.SlaveFile(self, task, path)
