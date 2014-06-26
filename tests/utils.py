
import functools
import json
import mock
import os
import sys
import unittest

def get_state(name, parse=True):
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", name))
    with open(path, "rb") as fobj:
        val = fobj.read()
        if parse:
            return json.loads(val)
        else:
            return val

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
