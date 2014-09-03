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
import re

import mock

import mesos.cli.cmds.events

from .. import utils


@mock.patch("mesos.cli.mesos_file.File._fetch", utils.sandbox_read)
class TestEvents(utils.MockState):

    @utils.patch_args([
        "mesos-events",
        "--sleep-interval=0.1"
    ])
    @mock.patch("mesos.cli.cmds.events.FOLLOW", False)
    @mock.patch("mesos.cli.cmds.events.POSITION", os.SEEK_SET)
    def test_stream(self):
        mesos.cli.cmds.events.main()

        assert len(re.findall("/slave/log", self.stdout)) == 2
        assert len(re.findall("/master/log", self.stdout)) == 1
