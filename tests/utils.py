
import functools
import json
import mock
import os
import sys
import unittest

import mesos_cli
import mesos_cli.exceptions

def get_state(name, parse=True):
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", name))
    with open(path, "rb") as fobj:
        val = fobj.read()
        if parse:
            return json.loads(val)
        else:
            return val

def sandbox_file(path):
    fpath = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", "sandbox", os.path.basename(path)))
    if not os.path.exists(fpath):
        raise mesos_cli.exceptions.FileDNE("")
    return open(fpath, "rb")

# Emulate the byte fetch interface and replace with reading local files
def sandbox_read(self):
    # This is an invalid path and the file does not exist.
    if not self._params["path"].startswith("/tmp/mesos"):
        raise mesos_cli.exceptions.FileDNE("")

    with sandbox_file(self._params["path"]) as fobj:
        if self._params["offset"] == -1:
            fobj.seek(0, os.SEEK_END)
            return {
                "data": "",
                "offset": fobj.tell()
            }

        fobj.seek(self._params["offset"])
        return {
            "data": fobj.read(self._params["length"]),
            "offset": self._params["offset"]
        }

browse_state = None
def file_list(self, path):
    if not globals()["browse_state"]:
        globals()["browse_state"] = get_state("browse.json")
    return globals()["browse_state"].get(path, [])

slave_stats = mock.PropertyMock(return_value=get_state("slave_statistics.json"))

patch_args = functools.partial(mock.patch, "sys.argv")

class MockState(unittest.TestCase):

    def setUp(self):
        self.mock(
            "mesos_cli.master.MesosMaster.state",
            get_state("master_state.json"))
        self.mock(
            "mesos_cli.slave.MesosSlave.state",
            get_state("slave-20140619-151434-16842879-5050-1196-0.json"))

    def mock(self, obj, val):
        m = mock.patch(obj, val)
        m.start()
        self.addCleanup(m.stop)

    @property
    def stdout(self):
        return sys.stdout.getvalue()

    @property
    def lines(self):
        return self.stdout.split("\n")
