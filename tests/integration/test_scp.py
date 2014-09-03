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


from __future__ import absolute_import, print_function

import mock

import mesos.cli.cmds.scp

from .. import utils


class TestScp(utils.MockState):

    @utils.patch_args([
        "mesos-scp",
        "stdout",
        "/tmp"
    ])
    def test_single(self):
        with mock.patch("subprocess.check_call", return_value=0) as m:
            mesos.cli.cmds.scp.main()

            m.assert_called_with(
                ["scp", "-pr", "stdout", "10.141.141.10:/tmp"])
            assert len(self.lines) == 3
            assert "uploaded" in self.stdout

    @utils.patch_args([
        "mesos-scp",
        "stdout",
        "stderr",
        "/tmp"
    ])
    def test_multiple(self):
        with mock.patch("subprocess.check_call", return_value=0):
            mesos.cli.cmds.scp.main()

            assert len(self.lines) == 5
            assert "uploaded" in self.stdout
