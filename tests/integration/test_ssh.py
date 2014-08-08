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

import mock

import mesos.cli.cmds.ssh

from .. import utils

DIR = os.path.join(
    '/tmp', 'mesos',
    'slaves', '20140619-151434-16842879-5050-1196-0',
    'frameworks', '20140612-230025-16842879-5050-1151-0000',
    'executors', 'app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2',
    'runs', '3db4a3e8-52c7-4b3f-8a30-f9cb0dc3d6ba'
)


class TestSsh(utils.MockState):

    @utils.patch_args([
        "mesos-ssh",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_sandbox(self):
        with mock.patch("os.execvp") as m:
            mesos.cli.cmds.ssh.main()

            m.assert_called_with("ssh", [
                'ssh',
                '-t',
                '10.141.141.10',
                'cd {0} && bash'.format(DIR)
            ])

    @utils.patch_args([
        "mesos-ssh",
        "app-215.2e6508c3-fafd-11e3-a955-b6f6cc110ef2"
    ])
    def test_missing(self):
        with mock.patch("os.execvp") as m:
            mesos.cli.cmds.ssh.main()

            m.assert_called_with("ssh", [
                'ssh',
                '-t',
                '10.141.141.10'
            ])

    @utils.patch_args([
        "mesos-ssh",
        "a"
    ])
    def test_partial(self):
        self.assertRaises(SystemExit, mesos.cli.cmds.ssh.main)

        assert len(self.lines) == 17
