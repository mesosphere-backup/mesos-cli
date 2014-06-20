
import itertools
import re
import time

def merge(obj, *keys):
    return itertools.chain(*[obj[k] for k in keys])

def iter_until(func, pre=lambda x: False, post=lambda x: False):
    while 1:
        val = func()
        if pre(val):
            break
        yield val
        if post(val):
            break

class cached_property(object):

    def __init__(self, ttl=300):
        self.ttl = ttl

    def __call__(self, fget, doc=None):
        self.fget = fget
        self.__doc__ = doc or fget.__doc__
        self.__name__ = fget.__name__
        self.__module__ = fget.__module__
        return self

    def __get__(self, inst, owner):
        now = time.time()
        try:
            value, last_update = inst._cache[self.__name__]
            if self.ttl > 0 and now - last_update > self.ttl:
                raise AttributeError
        except (KeyError, AttributeError):
            value = self.fget(inst)
            try:
                cache = inst._cache
            except AttributeError:
                cache = inst._cache = {}
            cache[self.__name__] = (value, now)
        return value
