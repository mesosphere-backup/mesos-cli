
import itertools

def merge(obj, *keys):
    return itertools.chain(*[obj[k] for k in keys])

def iter_until(func, predicate):
    while 1:
        val = func()
        yield val
        if predicate(val):
            break
