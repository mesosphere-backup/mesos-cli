
import itertools
import os

from . import slave
from . import util

CHUNK = 1024

class FileDNE(Exception):
    pass

class SlaveFile(object):

    def __init__(self, s, t, f):
        self._slave = s
        self._task = t
        self.fname = f
        self._slave_path = os.path.join(self._task.directory, f)
        self._offset = 0

        # Used during fetch, class level so the dict isn't constantly alloc'd
        self._params = {
            "path": self._slave_path,
            "offset": -1,
            "length": CHUNK
        }

    def __iter__(self):
        for l in self._readlines():
            yield l

    def __reversed__(self):
        for i, l in enumerate(self._readlines_reverse()):
            # Don't include the terminator when reading in reverse.
            if i == 0 and l == "":
                continue
            yield l

    def _fetch(self):
        resp = slave.fetch(self._slave, "/files/read.json", params=self._params)
        if resp.status_code == 404:
            raise FileDNE("No such file or directory.")
        return resp.json()

    def name(self):
        return "%s:%s/%s" % (self._slave["pid"], self._task.id, self.fname)

    def exists(self):
        try:
            self._fetch()
            return True
        except FileDNE:
            return False

    def size(self):
        self.last_size = self._fetch()["offset"]
        return self.last_size

    def seek(self, offset, whence=os.SEEK_SET):
        if whence == os.SEEK_SET:
            self._offset = 0 + offset
        elif whence == os.SEEK_CUR:
            self._offset += offset
        elif whence == os.SEEK_END:
            self._offset = self.size() + offset

    def tell(self):
        return self._offset

    def _length(self, start, size):
        if size and self.tell() - start + CHUNK > size:
            return size - (self.tell() - start)
        return CHUNK

    def _get_chunk(self, loc, size=CHUNK):
        self._params["offset"] = loc
        self._params["length"] = size

        data = self._fetch()["data"]
        self.seek(len(data), os.SEEK_CUR)
        return data

    def _read(self, size=None):
        start = self.tell()

        fn = lambda: self._get_chunk(
            self.tell(),
            size=self._length(start, size))
        pre = lambda x: x == ""
        post = lambda x: size and (self.tell() - start) >= size

        for blob in util.iter_until(fn, pre, post):
            yield blob

    def _read_reverse(self, size=None):
        fsize = self.size()
        if not size:
            size = fsize

        blocks = itertools.imap(lambda x: x,
            xrange(fsize - CHUNK, fsize - size, -CHUNK))

        try:
            while 1:
                yield self._get_chunk(blocks.next())
        except StopIteration:
            pass

        yield self._get_chunk(fsize - size, size % CHUNK)

    def read(self, size=None):
        return ''.join(self._read(size))

    def readline(self, size=None):
        for l in self._readlines(size):
            return l

    def _readlines(self, size=None):
        last = ""
        for blob in self._read(size):

            # This is not streaming and assumes small chunk sizes
            blob_lines = (last + blob).split("\n")
            for l in itertools.islice(blob_lines, 0, len(blob_lines) - 1):
                yield l

            last = blob_lines[-1]

    def _readlines_reverse(self, size=None):
        buf = ""
        for blob in self._read_reverse(size):

            blob_lines = (blob + buf).split("\n")
            for l in itertools.islice(
                    reversed(blob_lines), 0, len(blob_lines) - 1):
                yield l

            buf = blob_lines[0]

    def readlines(self, size=None):
        return list(self._readlines(size))
