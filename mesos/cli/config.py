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

import os
import json
import errno

class Config(dict):

    DEFAULTS = {
        "master": "localhost:5050",
        "log_level": "warning",
        "log_file": None
    }

    def __init__(self):
        self.update(self.DEFAULTS)
        self.load()

    def _get_path(self):
        return os.environ.get(
            'MESOS_CONFIG',
            os.path.expanduser('~/.mesos.json'))

    def __getattr__(self, item):
        return self[item]

    def load(self):
        try:
            with open(self._get_path(), 'rt') as f:
                try:
                    data = json.load(f)
                except ValueError as e:
                    raise ValueError(
                        'Invalid %s JSON: %s [%s]' %
                        (type(self).__name__, e.message, self.path)
                    )
                self.update(data)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise

def main():
    print json.dumps(Config(), indent=4)
