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

import argparse
import functools
import logging
import os

import blessings

import mesos.cli

from . import log
from .cfg import CURRENT as CFG
from .parser import ArgumentParser


def init(arg):
    # arg is:
    # @cli.init         : the function to be decorated
    # @cli.init(parser) : the parsing function
    is_parser = not callable(arg)

    def decorator(fn):
        @handle_signals
        @log.duration
        @functools.wraps(fn)
        def wrapper(*args, **kwargs):
            log_level = getattr(logging, CFG["log_level"].upper())
            logging.basicConfig(
                level=log_level,
                filename=CFG["log_file"]
            )

            if CFG["debug"] == "true":
                debug_requests()

            cmd_args = arg.parse_args() if is_parser else None
            return fn(cmd_args, *args, **kwargs)
        return wrapper

    if callable(arg):
        return decorator(arg)
    else:
        return decorator


def parser(**kwargs):
    parser_inst = ArgumentParser(
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
        **kwargs
    )

    parser_inst.add_argument(
        "-v", "--version",
        action="version", version="%(prog)s {0}".format(mesos.cli.__version__)
    )
    return parser_inst


def handle_signals(fn):
    @functools.wraps(fn)
    def wrapper(*args, **kwargs):
        try:
            return fn(*args, **kwargs)
        except KeyboardInterrupt:
            if CFG["debug"] == "true":
                raise
    return wrapper


def header(name):
    term = blessings.Terminal()
    print("==>" + term.red(str(name)) + "<==")


def cmds(short=False):
    def fltr(cmd):
        if not cmd.startswith("mesos-"):
            return False
        if cmd.endswith(".sh"):
            return False
        return True

    cmds = set([])
    for path in os.environ.get("PATH").split(os.pathsep):
        try:
            cmds = cmds.union(filter(fltr, os.listdir(path)))
        except OSError:
            pass

    if short:
        cmds = [x.split("-", 1)[-1] for x in cmds]

    return sorted(cmds)

last_seen = None


def output_file(seq, show_header=True, key=None):
    global last_seen

    if not key:
        key = str(seq)

    first = True
    for line in seq:
        if first and key != last_seen and show_header:
            header(key)

        # TODO(thomasr) - It is possible for there to be a pause in
        # the middle of this loop (reading the next block from the
        # remote) in this case, the header wouln't be printed and the
        # user would be confused.
        print(line)

        first = False

    if not first:
        last_seen = key


def debug_requests():
    try:
        import http.client as http_client
    except ImportError:
        # Python 2
        import httplib as http_client
    http_client.HTTPConnection.debuglevel = 1
