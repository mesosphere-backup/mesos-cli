
import contextlib
import kazoo.client
import kazoo.exceptions
import kazoo.handlers.threading

TIMEOUT = 1

# Helper for testing
client_class = kazoo.client.KazooClient

@contextlib.contextmanager
def client(*args, **kwargs):
    zk = client_class(*args, **kwargs)
    zk.start(timeout=TIMEOUT)
    try:
        yield zk
    finally:
        zk.stop()
