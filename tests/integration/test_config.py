
import json
import mock
import os
import sys

import mesos.cli.config

from .. import utils

config_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "config.json"))

class TestConfig(utils.MockState):

    @mock.patch('os.environ', { "mesos.cli_CONFIG": config_path })
    def test_output(self):
        mesos.cli.config.main()

        assert "master" in json.loads(self.stdout)
