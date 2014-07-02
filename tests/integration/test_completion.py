
import mock
import os
import StringIO
import sys

import mesoscli.completion

from .. import utils

def generate_env(line):
    env = {
        "COMP_LINE": line,
        "COMP_POINT": len(line)
    }
    env.update(os.environ)
    return env

# There are some side effects in completion. To test completers, make sure you
# use different commands. Otherwise, you'll get what appears to be random
# failures.
@mock.patch("mesoscli.completion.EXIT", sys.exit)
class TestCompletion(utils.MockState):

    @mock.patch("os.environ", generate_env("mesos "))
    def test_cmds(self):
        mesoscli.completion.main()

        assert "help" in self.stdout

    @mock.patch("os.environ", generate_env("mesos cat "))
    def test_task(self):
        self.assertRaises(SystemExit, mesoscli.completion.main)

        assert "app-15" in self.stdout
        assert "app-215" in self.stdout

        reload(mesoscli.cat)

    @mock.patch("os.environ", generate_env("mesos state 2"))
    def test_slave(self):
        self.assertRaises(SystemExit, mesoscli.completion.main)

        assert len(self.stdout.split("\n")) == 2

        reload(mesoscli.state)

    @mock.patch("os.environ", generate_env("mesos ls app-215 Twisted-14.0.0/"))
    @mock.patch("mesoscli.slave.MesosSlave.file_list", utils.file_list)
    def test_file(self):
        self.assertRaises(SystemExit, mesoscli.completion.main)

        assert "twisted/" in self.stdout
        assert "NEWS" in self.stdout

        reload(mesoscli.ls)
