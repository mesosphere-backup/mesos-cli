
import functools
import json
import mock
import os
import unittest

def get_state(name):
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", name))
    with open(path, "rb") as fobj:
        return json.loads(fobj.read())

class MockMaster(unittest.TestCase):

    def setUp(self):
        state = mock.patch("mesos_cli.master.MesosMaster.state",
            get_state("master_state.json"))
        state.start()
        self.addCleanup(state.stop)
