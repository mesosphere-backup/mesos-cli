
import os
import requests
import urlparse

from . import log
from .master import current as master
from . import slave
from . import slave_file

def directory(t):
    return slave.executor(
        slave.state(master.slave(t["slave_id"])),
        t["id"])["directory"]

def files(fltr, flist):
    tlist = master.tasks(fltr)
    mult = len(tlist) > 1 or len(flist) > 1
    dne = True

    for t in tlist:
        s = master.slave(t["slave_id"])
        d = directory(t)
        for f in flist:
            fobj = slave_file.SlaveFile(s, t, d, f)
            if fobj.exists():
                dne = False
                yield (s, t, fobj, mult)

    if dne:
        log.fatal("No such task has the requested file or directory")
