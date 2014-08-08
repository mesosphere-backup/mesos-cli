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

from .. import cli
from ..cfg import CURRENT as CFG

parser = cli.parser(
    description="interact with your local cli configuration"
)

parser.add_argument(
    "key", nargs="?", choices=CFG.DEFAULTS.keys() + ["profile"])

parser.add_argument("value", nargs="?")


@cli.handle_signals
def main():
    args = cli.init(parser)

    if args.key:
        if args.value:
            CFG[args.key] = args.value
            CFG.save()
        else:
            print(CFG[args.key])
    else:
        print(CFG)
