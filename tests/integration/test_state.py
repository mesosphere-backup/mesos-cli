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


import json
import mock
import os
import unittest

import mesos.cli.state

from .. import utils

class TestState(utils.MockState):

    @utils.patch_args([ "mesos-state" ])
    def test_master(self):
        mesos.cli.state.main()
        assert "version" in json.loads(self.stdout)

    @utils.patch_args([ "mesos-state", "20140619-151434-16842879-5050-1196-0" ])
    def test_single_slave(self):
        mesos.cli.state.main()

        val = json.loads(self.stdout)
        assert len(val) == 1
        assert val[0]["id"] == "20140619-151434-16842879-5050-1196-0"

    @utils.patch_args([ "mesos-state", "2" ])
    def test_partial_match(self):
        mesos.cli.state.main()

        val = json.loads(self.stdout)
        assert len(val) == 2
