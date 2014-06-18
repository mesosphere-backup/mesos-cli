
import os

from . import slave
from . import util

CHUNK = 1024

class SlaveFile(object):

    def __init__(self, s, p):
        self._slave = s
        self._path = p
        self._offset = 0

        # Used during fetch, class level so the dict isn't constantly alloc'd
        self._params = {
            "path": self._path,
            "offset": -1,
            "length": CHUNK
        }

    def __iter__(self):
        for blob in self.read():
            yield blob

    def _fetch(self):
        resp = slave.fetch(self._slave, "/files/read.json", params=self._params)
        if resp.status_code == 404:
            log.fatal("No such file or directory.")
        return resp.json()

    def _read(self, size=CHUNK):
        self._params["offset"] = self.tell()
        self._params["length"] = size

        data = self._fetch()["data"]
        self.seek(len(data), os.SEEK_CUR)
        return data

    def size(self):
        return self._fetch()["offset"]

    def _length(self, start, size):
        if size and self.tell() - start + CHUNK > size:
            return size - (self.tell() - start)
        return CHUNK

    def read(self, size=None):
        start = self.tell()

        fn = lambda: self._read(size=self._length(start, size))
        predicate = lambda x: (x == "" or
            (size and (self.tell() - start) >= size))

        for blob in util.iter_until(fn, predicate):
            yield blob

    def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._offset = 0 + offset
        elif whence == os.SEEK_CUR:
            self._offset += offset
        elif whence == os.SEEK_END:
            self._offset = self.size() + offset

    def tell(self):
        return self._offset
