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
import sys

import mesos.cli.config

from .. import utils

config_path = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "config.json"))

class TestConfig(utils.MockState):

    @mock.patch('os.environ', { "mesos.cli_CONFIG": config_path })
    def test_output(self):
        mesos.cli.config.main()

        assert "master" in json.loads(self.stdout)
