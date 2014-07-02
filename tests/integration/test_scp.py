
import mock

import mesos.cli.scp

from .. import utils

class TestScp(utils.MockState):

    @utils.patch_args([
        "mesos-scp",
        "stdout",
        "/tmp"
    ])
    def test_single(self):
        with mock.patch("gevent.subprocess.check_call", return_value=0) as m:
            mesos.cli.scp.main()

            m.assert_called_with(
                [ "scp", "-pr", "stdout", "10.141.141.10:/tmp" ])
            assert len(self.lines) == 3
            assert "uploaded" in self.stdout

    @utils.patch_args([
        "mesos-scp",
        "stdout",
        "stderr",
        "/tmp"
    ])
    def test_multiple(self):
        with mock.patch("gevent.subprocess.check_call", return_value=0):
            mesos.cli.scp.main()

            assert len(self.lines) == 5
            assert "uploaded" in self.stdout


