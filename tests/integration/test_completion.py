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
import os
import StringIO
import sys

import mesos.cli.cmds.completion

from .. import utils

def generate_env(line):
    env = {
        "COMP_LINE": line,
        "COMP_POINT": len(line)
    }
    env.update(os.environ)
    return env

# There are some side effects in completion. To test completers, make sure you
# use different commands. Otherwise, you'll get what appears to be random
# failures.
@mock.patch("mesos.cli.cmds.completion.EXIT", sys.exit)
class TestCompletion(utils.MockState):

    @mock.patch("os.environ", generate_env("mesos "))
    def test_cmds(self):
        mesos.cli.cmds.completion.main()

        assert "help" in self.stdout

    @mock.patch("os.environ", generate_env("mesos cat "))
    def test_task(self):
        self.assertRaises(SystemExit, mesos.cli.cmds.completion.main)

        assert "app-15" in self.stdout
        assert "app-215" in self.stdout

        reload(mesos.cli.cmds.cat)

    @mock.patch("os.environ", generate_env("mesos state 2"))
    def test_slave(self):
        self.assertRaises(SystemExit, mesos.cli.cmds.completion.main)

        assert len(self.stdout.split("\n")) == 2

        reload(mesos.cli.cmds.state)

    @mock.patch("os.environ", generate_env("mesos ls app-215 Twisted-14.0.0/"))
    @mock.patch("mesos.cli.slave.MesosSlave.file_list", utils.file_list)
    def test_file(self):
        self.assertRaises(SystemExit, mesos.cli.cmds.completion.main)

        assert "twisted/" in self.stdout
        assert "NEWS" in self.stdout

        reload(mesos.cli.cmds.ls)
