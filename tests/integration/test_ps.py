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


import mock

import mesos.cli.cmds.ps

from .. import utils


@mock.patch("mesos.cli.slave.MesosSlave.stats", utils.slave_stats)
class TestPs(utils.MockState):

    @utils.patch_args([
        "mesos-ps"
    ])
    def test_format(self):
        mesos.cli.cmds.ps.main()

        # Time
        assert "01:23.33" in self.stdout
        # RSS
        assert "10.46 MB" in self.stdout
        # CPU
        assert "0.1" in self.stdout
        # MEM
        assert "65.41" in self.stdout
        # Command
        assert "while true" in self.stdout
        # User
        assert "root" in self.stdout
        # PID
        assert "app-215.3e" in self.stdout

        assert len(self.lines) == 4

    @utils.patch_args([
        "mesos-ps",
        "-i"
    ])
    def test_inactive(self):
        mesos.cli.cmds.ps.main()

        assert len(self.lines) == 17
