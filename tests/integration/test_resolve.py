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

import os

import zake.fake_client
import zake.fake_storage

import mesos.cli.cmds.resolve

from .. import utils

master_file = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "master-host"))


class TestResolve(utils.MockState):

    def setUp(self):  # noqa
        super(utils.MockState, self).setUp()

        self.init_zk()

    def init_zk(self):
        self.storage = zake.fake_storage.FakeStorage()
        self.zk = zake.fake_client.FakeClient(storage=self.storage)
        self.zk.start()
        self.addCleanup(self.zk.stop)

        zk = zake.fake_client.FakeClient(storage=self.storage)
        self.mock(
            "mesos.cli.zookeeper.client_class",
            lambda *args, **kwargs: zk)

        self.zk.create(
            "/mesos/info_0000000008",
            utils.get_state("master.pb", parse=False),
            makepath=True)

    @utils.patch_args(["mesos-resolve", "localhost:5050"])
    def test_tcp(self):
        mesos.cli.cmds.resolve.main()

        assert self.stdout == "localhost:5050\n"

    @utils.patch_args(["mesos-resolve", "zk://localhost:5050/mesos"])
    def test_zk(self):
        mesos.cli.cmds.resolve.main()

        assert self.stdout == "10.141.141.10:5050\n"

    @utils.patch_args(["mesos-resolve", "file:///" + master_file])
    def test_file(self):
        mesos.cli.cmds.resolve.main()

        assert self.stdout == "10.141.141.10:5050\n"
