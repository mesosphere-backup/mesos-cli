
import datetime
import os
import re
import requests
import urlparse

from . import exceptions
from . import log
from . import slave
from . import slave_file
from . import util

class Task(dict):

    cmd_re = re.compile("\(Command: (.+)\)")

    def __init__(self, master, meta):
        self.master = master
        self._meta = meta

    def __str__(self):
        return "{}:{}".format(
            self.slave.pid.split('@')[-1].split(':')[0], self.id)

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
        return slave_file.SlaveFile(self.slave, self, path)

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

def files(fltr, flist):
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

    if dne:
        log.fatal("No such task has the requested file or directory")
