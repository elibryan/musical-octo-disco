from collections.abc import Iterable
import pandas as pd
import numpy as np


def get_in(m, path, default=None):
    if not path:
        return m
    if not isinstance(m, dict):
        return default
    if path[0] not in m:
        return default
    return get_in(m[path[0]], path[1:], default)


def assoc_in(m, keys, v):
    if 0 == len(keys):
        return v
    m[keys[0]] = assoc_in(m.get(keys[0], {}), keys[1:], v)
    return m


def is_nil_or_empty(v):
    return (
            v is None
            or (isinstance(v, list) and 0 == len(v))
            or (isinstance(v, set) and 0 == len(v))
            or (isinstance(v, dict) and 0 == len(v.keys()))
            or (isinstance(v, str) and 0 == len(v))
            or (isinstance(v, float) and pd.isna(v))
            or (isinstance(v, float) and np.nan == v)
    )


def flatten(xs):
    for x in xs:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            yield from flatten(x)
        else:
            yield x


def to_flat_list(v):
    if is_nil_or_empty(v):
        return []
    if isinstance(v, str) or isinstance(v, int) or isinstance(v, float):
        return [v]
    if isinstance(v, list) or isinstance(v, np.ndarray):
        return list(flatten(v))
    if isinstance(v, set):
        return list(v)
    if isinstance(v, pd.Timestamp):
        return [v]
    else:
        print(type(v))
        return [v]


def to_unique_list(vs, key=lambda v: v):
    output = []
    seen = set([])
    for v in vs:
        if key(v) not in seen:
            output.append(v)
            seen.add(key(v))
    return output
