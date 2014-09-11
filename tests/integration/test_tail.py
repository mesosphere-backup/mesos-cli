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

import re

import mock

import mesos.cli.cmds.tail

from .. import utils


@mock.patch("mesos.cli.mesos_file.File._fetch", utils.sandbox_read)
class TestTail(utils.MockState):

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single_default(self):
        mesos.cli.cmds.tail.main()

        assert len(self.lines) == 6

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stderr"
    ])
    def test_single_specific(self):
        mesos.cli.cmds.tail.main()

        assert len(self.lines) == 9

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "st"
    ])
    def test_partial(self):
        self.assertRaises(SystemExit, mesos.cli.cmds.tail.main)

        assert len(self.lines) == 2

    @utils.patch_args([
        "mesos-tail",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos.cli.cmds.tail.main()

        assert len(self.lines) == 11

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout",
        "stderr"
    ])
    def test_multiple_files(self):
        mesos.cli.cmds.tail.main()

        assert len(re.findall("==>", self.stdout)) == 2
        assert len(self.lines) == 14

    @utils.patch_args([
        "mesos-tail",
        "-n", "1",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_line_limit(self):
        mesos.cli.cmds.tail.main()

        assert "Forked" in self.stdout
        assert len(self.lines) == 3

    @utils.patch_args([
        "mesos-tail",
        "-q",
        "app"
    ])
    def test_hide_header(self):
        mesos.cli.cmds.tail.main()

        assert len(self.lines) == 9
