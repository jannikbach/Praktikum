from itertools import groupby

import networkx as nx


def split_by_key(cluster, key_func):
    representative, graphs = cluster
    graphs.sort(key=key_func)
    return [(key, list(group)) for key, group in groupby(graphs, key=key_func)]



def split_by_equality(cluster, is_equal, representative_func=None):
    representative, graphs = cluster
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

    return clusters


def node_match(n1, n2):
    """
    Check if two nodes should be considered identical
    """
    return n1['element'] == n2['element'] and n1['charge'] == n2['charge']


def edge_match(e1, e2):
    """
    Check if two edges should be considered identical
    """
    return e1['order'] == e2['order']


def is_isomorphic(rc1, rc2):
    """
    Check if two reaction centers are isomorphic.
    """
    return nx.is_isomorphic(rc1, rc2, node_match=node_match, edge_match=edge_match)


def get_rc(G: nx.Graph) -> nx.Graph:
    edges = [(e[0], e[1]) for e in G.edges(data=True) if e[2]["standard_order"] != 0]
    return nx.edge_subgraph(G, edges)


