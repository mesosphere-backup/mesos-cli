
import mock

import mesos.cli.find

from .. import utils

@mock.patch("mesos.cli.slave.MesosSlave.file_list", utils.file_list)
class TestFind(utils.MockState):

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single(self):
        mesos.cli.find.main()

        assert len(self.lines) == 3

    @utils.patch_args([
        "mesos-find",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "Twisted-14.0.0/twisted/words/xish/"
    ])
    def test_path(self):
        mesos.cli.find.main()

        assert len(self.lines) == 8

    @utils.patch_args([
        "mesos-find",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos.cli.find.main()

        assert len(self.lines) == 1872

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "std"
    ])
    def test_partial(self):
        mesos.cli.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "app-15.41fef02d-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_exact(self):
        mesos.cli.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "-q",
        "app",
        "std"
    ])
    def test_hide_header(self):
        mesos.cli.find.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-find",
        "app",
        "std"
    ])
    def test_empty_files(self):
        mesos.cli.find.main()

        assert len(self.lines) == 16
