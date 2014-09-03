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
import testtools

import mesos.cli.master

from .. import utils

config = {
    "master": "foo:5050",
    "scheme": "https"
}


class TestMaster(utils.MockState):

    @mock.patch.object(mesos.cli.master, 'CFG', config)
    def test_scheme(self):
        assert 'https' in mesos.cli.master.CURRENT.host
