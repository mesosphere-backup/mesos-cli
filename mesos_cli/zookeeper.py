
import contextlib
import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

TIMEOUT = 1

@contextlib.contextmanager
def client(*args, **kwargs):
    zk = kazoo.client.KazooClient(*args, **kwargs)
    zk.start(timeout=TIMEOUT)
    try:
        yield zk
    finally:
        zk.stop()
