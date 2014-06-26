
import functools
import json
import mock
import os
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

class MockMaster(unittest.TestCase):

    def setUp(self):
        self.mock(
            "mesos_cli.master.MesosMaster.state",
            get_state("master_state.json"))

    def mock(self, obj, val):
        m = mock.patch(obj, val)
        m.start()
        self.addCleanup(m.stop)
