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

import mesos.cli.cmds.cat
import mesos.cli.exceptions

from .. import utils

@mock.patch("mesos.cli.slave_file.SlaveFile._fetch", utils.sandbox_read)
class TestCat(utils.MockState):

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single_default(self):
        mesos.cli.cmds.cat.main()

        assert len(self.lines) == 5

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stderr"
    ])
    def test_single_specific(self):
        mesos.cli.cmds.cat.main()

        assert len(self.lines) == 8

    @utils.patch_args([
        "mesos-cat",
        "app",
        "st"
    ])
    def test_partial(self):
        mesos.cli.cmds.cat.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-cat",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos.cli.cmds.cat.main()

        assert len(self.lines) == 9

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout",
        "stderr"
    ])
    def test_multiple_files(self):
        mesos.cli.cmds.cat.main()

        assert len(self.lines) == 12

    @utils.patch_args([
        "mesos-cat",
        "app-215.2a1d811b-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_missing(self):
        mesos.cli.cmds.cat.main()

        assert len(self.stdout) == 0
