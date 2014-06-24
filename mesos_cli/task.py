
import datetime
import os
import re
import requests
import urlparse

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
        return self.executor["directory"]

    @util.cached_property()
    def slave(self):
        return self.master.slave(self._meta["slave_id"])

    def file(self, path):
        return slave_file.SlaveFile(self.slave, self, path)

    def file_list(self, path):
        return self.slave.file_list(os.path.join(self.directory, path))

    @property
    def stats(self):
        return self.slave.task_stats(self.id)

    @property
    def cpu_time(self):
        st = self.stats
        secs = st["cpus_user_time_secs"] + \
            st["cpus_system_time_secs"]
        # timedelta has a resolution of .000000 while mesos only keeps .00
        return str(datetime.timedelta(seconds=secs))[:-4]

    @property
    def cpu_limit(self):
        return self.stats["cpus_limit"]

    @property
    def mem_limit(self):
        return self.stats["mem_limit_bytes"]

    @property
    def rss(self):
        return self.stats["mem_rss_bytes"]

    @property
    def command(self):
        result = self.cmd_re.search(self.executor["name"])
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
