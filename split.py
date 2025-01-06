from itertools import groupby


def split_by_key(graphs, key_func):
    graphs.sort(key=key_func)
    return [list(group) for key, group in groupby(graphs, key=key_func)]
