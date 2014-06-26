
import mock

import mesos_cli.ls

from .. import utils

@mock.patch("mesos_cli.slave.MesosSlave.file_list", utils.file_list)
class TestLs(utils.MockState):

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single(self):
        mesos_cli.ls.main()

        # mode
        assert "-rw-r--r-x" in self.stdout
        # user + group
        assert "root root" in self.stdout
        # size
        assert "231" in self.stdout
        # date
        assert "Jun 25 15:44" in self.stdout
        #name
        assert "stdout" in self.stdout

        assert len(self.lines) == 3

    @utils.patch_args([
        "mesos-ls",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "Twisted-14.0.0/"
    ])
    def test_path(self):
        mesos_cli.ls.main()

        assert len(self.lines) == 12

    @utils.patch_args([
        "mesos-ls",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos_cli.ls.main()

        assert len(self.lines) == 22

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "std"
    ])
    def test_partial(self):
        mesos_cli.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_exact(self):
        mesos_cli.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "-q",
        "app",
        "std"
    ])
    def test_hide_header(self):
        mesos_cli.ls.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-ls",
        "app",
        "std"
    ])
    def test_empty_files(self):
        mesos_cli.ls.main()

        assert len(self.lines) == 16
