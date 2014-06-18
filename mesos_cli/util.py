
import itertools

def merge(obj, *keys):
    return itertools.chain(*[obj[k] for k in keys])
