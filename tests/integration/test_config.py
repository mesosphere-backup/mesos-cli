
import json
import mock
import os
import sys

import mesos_cli.config

from .. import utils

config_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "config.json"))

class TestConfig(utils.MockMaster):

    @mock.patch('os.environ', { "MESOS_CLI_CONFIG": config_path })
    def test_output(self):
        mesos_cli.config.main()

        assert "master" in json.loads(sys.stdout.getvalue())
