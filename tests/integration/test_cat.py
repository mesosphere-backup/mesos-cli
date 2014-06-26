
import mock
import os

import mesos_cli.cat
import mesos_cli.exceptions

from .. import utils

@mock.patch("mesos_cli.slave_file.SlaveFile._fetch", utils.sandbox_read)
class TestCat(utils.MockState):

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single_default(self):
        mesos_cli.cat.main()

        assert len(self.lines) == 5

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stderr"
    ])
    def test_single_specific(self):
        mesos_cli.cat.main()

        assert len(self.lines) == 8

    @utils.patch_args([
        "mesos-cat",
        "app",
        "st"
    ])
    def test_partial(self):
        mesos_cli.cat.main()

        assert len(self.stdout) == 0

    @utils.patch_args([
        "mesos-cat",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos_cli.cat.main()

        assert len(self.lines) == 9

    @utils.patch_args([
        "mesos-cat",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout",
        "stderr"
    ])
    def test_multiple_files(self):
        mesos_cli.cat.main()

        assert len(self.lines) == 12

    @utils.patch_args([
        "mesos-cat",
        "app-215.2a1d811b-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout"
    ])
    def test_missing(self):
        mesos_cli.cat.main()

        assert len(self.stdout) == 0
