
import mock
import os
import sys
import zake.fake_client
import zake.fake_storage

import mesos_cli.resolve

from .. import utils

master_file = os.path.normpath(os.path.join(
    os.path.dirname(__file__), "..", "data", "master-host"))

class TestResolve(utils.MockMaster):

    def setUp(self):
        super(utils.MockMaster, self).setUp()

        self.init_zk()


    def init_zk(self):
        self.storage = zake.fake_storage.FakeStorage()
        self.zk = zake.fake_client.FakeClient(storage=self.storage)
        self.zk.start()
        self.addCleanup(self.zk.stop)

        zk = zake.fake_client.FakeClient(storage=self.storage)
        self.mock("mesos_cli.zookeeper.client_class",
            lambda *args, **kwargs: zk)

        self.zk.create("/mesos/info_0000000008",
            utils.get_state("master.pb", parse=False),
            makepath=True)

    @mock.patch("sys.argv", [ "mesos-resolve", "localhost:5050" ])
    def test_tcp(self):
        mesos_cli.resolve.main()

        assert sys.stdout.getvalue() == "localhost:5050\n"

    @mock.patch("sys.argv", [ "mesos-resolve", "zk://localhost:5050/mesos" ])
    def test_zk(self):
        mesos_cli.resolve.main()

        assert sys.stdout.getvalue() == "10.141.141.10:5050\n"

    @mock.patch("sys.argv", [ "mesos-resolve", "file:///" + master_file ])
    def test_file(self):
        mesos_cli.resolve.main()

        assert sys.stdout.getvalue() == "10.141.141.10:5050\n"
