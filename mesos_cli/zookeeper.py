
import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

class Client(object):

    TIMEOUT = 1

    def __init__(self, **kwargs):
        self.zk = kazoo.client.KazooClient(**kwargs)

    def __enter__(self):
        self.zk.start(timeout=self.TIMEOUT)
        return self.zk

    def __exit__(self, typ, val, tb):
        self.zk.stop()

        if typ != None:
            return False
