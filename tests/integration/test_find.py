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

import mesos.cli.cmds.find

from .. import utils


@mock.patch("mesos.cli.slave.MesosSlave.file_list", utils.file_list)
class TestFind(utils.MockState):

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single(self):
        mesos.cli.cmds.find.main()

        assert len(self.lines) == 3

    @utils.patch_args([
        "mesos-find",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "Twisted-14.0.0/twisted/words/xish/"
    ])
    def test_path(self):
        mesos.cli.cmds.find.main()

        assert len(self.lines) == 8

    @utils.patch_args([
        "mesos-find",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos.cli.cmds.find.main()

        assert len(self.lines) == 1872

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "std"
    ])
    def test_partial(self):
        mesos.cli.cmds.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_exact(self):
        mesos.cli.cmds.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "-q",
        "app",
        "std"
    ])
    def test_hide_header(self):
        mesos.cli.cmds.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "app",
        "std"
    ])
    def test_empty_files(self):
        mesos.cli.cmds.find.main()

        assert len(self.lines) == 16
