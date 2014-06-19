
import itertools
import re

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
