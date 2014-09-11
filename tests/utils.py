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

import functools
import json
import os
import sys

import mock
import testtools

import mesos.cli
import mesos.cli.cli
import mesos.cli.exceptions


def get_state(name, parse=True):
    path = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", name))
    with open(path, "rb") as fobj:
        val = fobj.read()
        if parse:
            return json.loads(val)
        else:
            return val


def sandbox_file(path):
    fpath = os.path.normpath(os.path.join(
        os.path.dirname(__file__), "data", "sandbox", os.path.basename(path)))
    if not os.path.exists(fpath):
        raise mesos.cli.exceptions.FileDoesNotExist("")
    return open(fpath, "rb")


# Emulate the byte fetch interface and replace with reading local files
def sandbox_read(self):
    # This is an invalid path and the file does not exist.
    if self._params["path"] not in ["/master/log", "/slave/log"] and \
            not self._params["path"].startswith("/tmp/mesos"):
        raise mesos.cli.exceptions.FileDoesNotExist("")

    with sandbox_file(self._params["path"]) as fobj:
        if self._params["offset"] == -1:
            fobj.seek(0, os.SEEK_END)
            return {
                "data": "",
                "offset": fobj.tell()
            }

        fobj.seek(self._params["offset"])
        return {
            "data": fobj.read(self._params["length"]),
            "offset": self._params["offset"]
        }

browse_state = None


def file_list(self, path):
    if not globals()["browse_state"]:
        globals()["browse_state"] = get_state("browse.json")
    return globals()["browse_state"].get(path, [])

slave_stats = mock.PropertyMock(
    return_value=get_state("slave_statistics.json"))

patch_args = functools.partial(mock.patch, "sys.argv")


class MockState(testtools.TestCase):

    def setUp(self):  # noqa
        super(MockState, self).setUp()
        self.mock(
            "mesos.cli.master.MesosMaster.state",
            get_state("master_state.json"))
        self.mock(
            "mesos.cli.slave.MesosSlave.state",
            get_state("slave-20140619-151434-16842879-5050-1196-0.json"))

    def tearDown(self):
        super(MockState, self).tearDown()
        mesos.cli.cli.last_seen = None

    def mock(self, obj, val):
        m = mock.patch(obj, val)
        m.start()
        self.addCleanup(m.stop)

    @property
    def stdout(self):
        return sys.stdout.getvalue()

    @property
    def lines(self):
        return self.stdout.split("\n")
