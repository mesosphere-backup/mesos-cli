
import itertools
import logging
import requests
import sys
import urlparse

from . import log
from . import util

FILE_CHUNK = 1024

def fetch(s, u, **kwargs):
    try:
        return requests.get(urlparse.urljoin(
            url(s), u), **kwargs)
    except requests.exceptions.ConnectionError:
        logging.error("Unable to connect to the slave at %s." % (url(s),))
        sys.exit(1)

def host(s):
    return s["pid"].split("@")[-1]

def url(s):
    return "http://" + host(s)

def state(s):
    return fetch(s, "/slave(1)/state.json").json()

def executor(s, i):
    for fw in s["frameworks"]:
        for exc in util.merge(fw, "executors", "completed_executors"):
            if i == exc["id"]:
                return exc
    raise Exception("No executor by that id")

def file_list(s, d):
    resp = fetch(s, "/files/browse.json", params={ "path": d })
    if resp.status_code == 404:
        return []
    return resp.json()

def file_size(s, d):
    resp = fetch(s, "/files/read.json", params={ "path": d, "offset": -1})
    if resp.status_code == 404:
        log.fatal("No such file or directory.")
    return resp.json()["offset"]

def file(s, d, offset=0, size=-1):
    if size == -1:
        size = file_size(s, d)

    progress = offset
    while progress < size:
        resp = fetch(s, "/files/read.json",
            params={ "path": d, "offset": progress }).json()
        progress += len(resp["data"])
        yield resp["data"]
