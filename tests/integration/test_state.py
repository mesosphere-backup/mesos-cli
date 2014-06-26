
import json
import mock
import os
import unittest

import mesos_cli.state

from .. import utils

class TestState(utils.MockState):

    @mock.patch("sys.argv", [ "mesos-state" ])
    def test_master(self):
        mesos_cli.state.main()
        assert "version" in json.loads(self.stdout)

    @mock.patch(
        "sys.argv", [ "mesos-state", "20140619-151434-16842879-5050-1196-0" ])
    def test_single_slave(self):
        mesos_cli.state.main()

        val = json.loads(self.stdout)
        assert len(val) == 1
        assert val[0]["id"] == "20140619-151434-16842879-5050-1196-0"

    @mock.patch("sys.argv", [ "mesos-state", "2" ])
    def test_partial_match(self):
        mesos_cli.state.main()

        val = json.loads(self.stdout)
        assert len(val) == 2
