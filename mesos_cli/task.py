
import os
import requests
import urlparse

from . import log
from . import slave
from . import slave_file
from . import util

class Task(dict):

    def __init__(self, master, meta):
        self.master = master
        self._meta = meta

    def __str__(self):
        return "{}:{}".format(self.slave.pid, self.id)

    def __getattr__(self, name):
        if name in self._meta:
            return self._meta[name]
        raise AttributeError()

    @util.cached_property()
    def directory(self):
        return self.slave.executor(self.id)["directory"]

    @util.cached_property()
    def slave(self):
        return self.master.slave(self._meta["slave_id"])

    def file(self, path):
        return slave_file.SlaveFile(self.slave, self, path)

    def file_list(self, path):
        return self.slave.file_list(os.path.join(self.directory, path))

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
