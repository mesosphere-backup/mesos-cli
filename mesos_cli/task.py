
import os
import requests
import urlparse

from . import log
from . import master
from . import slave
from . import slave_file

def directory(m, t):
    return slave.executor(
        slave.state(master.slave(m, t["slave_id"])),
        t["id"])["directory"]

def files(m, fltr, flist):
    tlist = master.tasks(m, fltr)
    mult = len(tlist) > 1 or len(args.file) > 1
    dne = True

    for t in tlist:
        s = master.slave(m, t["slave_id"])
        d = directory(m, t)
        for f in flist:
            fobj = slave_file.SlaveFile(s, d, f)
            if fobj.exists():
                dne = False
                yield (s, t, fobj, mult)

    if dne:
        log.fatal("No such task has the requested file or directory")
