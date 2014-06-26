
import mock

import mesos_cli.tail

from .. import utils

@mock.patch("mesos_cli.slave_file.SlaveFile._fetch", utils.sandbox_read)
class TestHead(utils.MockState):

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_single_default(self):
        mesos_cli.tail.main()

        assert len(self.lines) == 5

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stderr"
    ])
    def test_single_specific(self):
        mesos_cli.tail.main()

        assert len(self.lines) == 8

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "st"
    ])
    def test_partial(self):
        self.assertRaises(SystemExit, mesos_cli.tail.main)

        assert len(self.lines) == 1

    @utils.patch_args([
        "mesos-tail",
        "app"
    ])
    def test_multiple_tasks(self):
        mesos_cli.tail.main()

        assert len(self.lines) == 11

    @utils.patch_args([
        "mesos-tail",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2",
        "stdout",
        "stderr"
    ])
    def test_multiple_files(self):
        mesos_cli.tail.main()

        assert len(self.lines) == 14

    @utils.patch_args([
        "mesos-tail",
        "-n", "1",
        "app-215.3e6a099c-fcba-11e3-8b67-b6f6cc110ef2"
    ])
    def test_line_limit(self):
        mesos_cli.tail.main()

        assert "Forked" in self.stdout
        assert len(self.lines) == 2

    @utils.patch_args([
        "mesos-tail",
        "-q",
        "app"
    ])
    def test_hide_header(self):
        mesos_cli.tail.main()

        assert len(self.lines) == 9
