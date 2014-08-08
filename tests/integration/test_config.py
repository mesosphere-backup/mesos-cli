# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

import json
import os
import tempfile

import mock

import mesos.cli.cfg
import mesos.cli.cmds.config

from .. import utils

config_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "config.json"))


class TestConfig(utils.MockState):

    @mock.patch('os.environ', {"MESOS_CLI_CONFIG": config_path})
    @utils.patch_args(["mesos-config"])
    def test_output(self):
        mesos.cli.cmds.config.cfg = mesos.cli.cfg.Config()

        mesos.cli.cmds.config.main()

        out = json.loads(self.stdout)
        assert "master" in out["test"]

    @mock.patch('os.environ', {"MESOS_CLI_CONFIG": config_path})
    @utils.patch_args([
        "mesos-config",
        "master"
    ])
    def test_get_key(self):
        mesos.cli.cmds.config.cfg = mesos.cli.cfg.Config()

        mesos.cli.cmds.config.main()

        assert "zk://localhost:2181/mesos" in self.stdout

    @utils.patch_args([
        "mesos-config",
        "master",
        "zk://localhost:2181/mesos"
    ])
    def test_set_key(self):
        fd, fname = tempfile.mkstemp()
        with open(fname, "w") as fobj:
            fobj.write("{}")
        try:
            with mock.patch('os.environ', {"MESOS_CLI_CONFIG": fname}):
                mesos.cli.cmds.config.cfg = mesos.cli.cfg.Config()

                mesos.cli.cmds.config.main()

                with open(fname, "r") as fobj:
                    assert "zk://localhost:2181" in json.loads(
                        fobj.read())["default"]["master"]
        finally:
            os.remove(fname)
