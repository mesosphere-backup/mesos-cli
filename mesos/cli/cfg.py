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

import errno
import json
import os


class Config(dict):

    _default_profile = "default"

    DEFAULTS = {
        "master": "localhost:5050",
        "log_level": "warning",
        "log_file": None
    }

    cfg_name = ".mesos.json"

    search_path = [os.path.join(x, cfg_name) for x in [
        ".",
        os.path.expanduser("~"),
        "/etc",
        "/usr/etc",
        "/usr/local/etc"
    ]]

    def __init__(self):
        self.load()

    def _config_file(self):
        for p in self.search_path:
            if os.path.exists(p):
                return p

        # default to creating a user level config file
        return self.search_path[1]

    def _get_path(self):
        return os.environ.get(
            'MESOS_CLI_CONFIG', self._config_file())

    @property
    def _profile_key(self):
        return self.get("profile", self._default_profile)

    @property
    def _profile(self):
        return self.get(self._profile_key, {})

    def __getattr__(self, item):
        if item == "profile":
            return self[item]
        return self._profile.get(item, self.DEFAULTS[item])

    def __setattr__(self, k, v):
        base = self

        if k != "profile":
            if self._profile_key not in self.keys():
                self[self._profile_key] = {}
            base = self._profile

        base[k] = v

    def load(self):
        try:
            with open(self._get_path(), 'rt') as f:
                try:
                    data = json.load(f)
                except ValueError as e:
                    raise ValueError(
                        'Invalid %s JSON: %s [%s]' %
                        (type(self).__name__, e.message, self._get_path())
                    )
                self.update(data)
        except IOError as e:
            if e.errno != errno.ENOENT:
                raise

            # No config file exists, create the basic so that users can see the
            # available options
            self[self._default_profile] = self.DEFAULTS
            self["profile"] = self._default_profile

    def save(self):
        with open(self._get_path(), "wb") as f:
            f.write(json.dumps(self, indent=4))

current = Config()
