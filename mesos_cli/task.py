
import os
import requests
import urlparse

from . import master
from . import slave

def directory(m, t):
    return slave.executor(
        slave.state(master.slave(m, t["slave_id"])),
        t["id"])["directory"]

