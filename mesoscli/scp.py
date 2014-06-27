
import gevent.monkey
gevent.monkey.patch_all()

import gevent.subprocess
import itertools
import os

from . import cli
from .master import current as master
from . import log

parser = cli.parser(
    description="upload the specified local file(s) to all slaves"
)

parser.add_argument(
    "file", nargs="+",
    help="Local files to upload to the slaves"
)

parser.add_argument(
    "remote_path",
    help="Remote path to upload local files to"
)

def upload(slave, src, dst):
    cmd = [
        "scp",
        "-pr",
        src,
        "{}:{}".format(slave.hostname, dst)
    ]
    try:
        return (slave, src, dst, log.fn(gevent.subprocess.check_call, cmd))
    except gevent.subprocess.CalledProcessError, e:
        return (slave, e.returncode)

def main():
    cfg, args = cli.init(parser)

    jobs = list(itertools.chain(
        *[[gevent.spawn(upload, s, f, args.remote_path) for f in args.file]
            for s in master.slaves()]))

    gevent.joinall(jobs)

    for slave, src, dst, retcode in [x.value for x in jobs]:
        print "{}:{}\t{}".format(slave.hostname, os.path.join(dst, src),
            "uploaded" if retcode == 0 else "failed")
