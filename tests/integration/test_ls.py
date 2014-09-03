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

import mesos.cli.cmds.ls

from .. import utils


@mock.patch("mesos.cli.slave.MesosSlave.file_list", utils.file_list)
class TestLs(utils.MockState):

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single(self):
        mesos.cli.cmds.ls.main()

        # mode
        assert "-rw-r--r-x" in self.stdout
        # user + group
        assert "root root" in self.stdout
        # size
        assert "231" in self.stdout
        # date
        assert "Jun 25 15:44" in self.stdout
        # name
        assert "stdout" in self.stdout

        assert len(self.lines) == 3

    @utils.patch_args([
        "mesos-ls",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "Twisted-14.0.0/"
    ])
    def test_path(self):
        mesos.cli.cmds.ls.main()

        assert len(self.lines) == 12

    @utils.patch_args([
        "mesos-ls",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos.cli.cmds.ls.main()

        assert len(self.lines) == 22

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "std"
    ])
    def test_partial(self):
        mesos.cli.cmds.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_exact(self):
        mesos.cli.cmds.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "-q",
        "app",
        "std"
    ])
    def test_hide_header(self):
        mesos.cli.cmds.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "app",
        "std"
    ])
    def test_empty_files(self):
        mesos.cli.cmds.ls.main()

        assert len(self.lines) == 16
