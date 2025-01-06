from itertools import groupby


def split_by_key(graphs, key_func):
    graphs.sort(key=key_func)
    return [list(group) for key, group in groupby(graphs, key=key_func)]


def split_by_equality(graphs, is_equal, representative_func):
    if representative_func is None:
        # use identity
        representative_func = lambda x: x

    clusters = []

    for graph in graphs:
        representative = representative_func(graph)

        found_cluster = False
        for cluster_representative, cluster_elements in clusters:
            if is_equal(representative, cluster_representative):
                cluster_elements.append(graph)
                found_cluster = True
                break

        if not found_cluster:
            # spawn new cluster
            # use representative of the first element as representative of the whole cluster
            cluster = (representative, [graph])
            clusters.append(cluster)

    # drop representatives
    return [elements for representative, elements in clusters]
