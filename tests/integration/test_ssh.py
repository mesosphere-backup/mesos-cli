
import mock

import mesos_cli.ssh

from .. import utils

class TestSsh(utils.MockState):

    @utils.patch_args([
        "mesos-ssh",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_sandbox(self):
        with mock.patch("os.execvp") as m:
            mesos_cli.ssh.main()

            m.assert_called_with("ssh", [
                'ssh',
                '-t',
                '10.141.141.10',
                'cd /tmp/mesos/slaves/20140619-151434-16842879-5050-1196-0/frameworks/20140612-230025-16842879-5050-1151-0000/executors/app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2/runs/3db4a3e8-52c7-4b3f-8a30-f9cb0dc3d6ba && bash'
            ])

    @utils.patch_args([
        "mesos-ssh",
        "app-215.2e6508c3-fafd-11e3-a955-b6f6cc110ef2"
    ])
    def test_missing(self):
        with mock.patch("os.execvp") as m:
            mesos_cli.ssh.main()

            m.assert_called_with("ssh", [
                'ssh',
                '-t',
                '10.141.141.10'
            ])

    @utils.patch_args([
        "mesos-ssh",
        "a"
    ])
    def test_partial(self):
        self.assertRaises(SystemExit, mesos_cli.ssh.main)

        assert len(self.lines) == 17
