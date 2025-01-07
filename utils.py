import time
import pickle
from itertools import groupby

import more_itertools
import networkx as nx
from tqdm import tqdm


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


def partition_clusters_by_invariant(clusters, invariant):
    """
    Partition clusters by invariant
    """
    partitioned_clusters = []
    for cluster in clusters:
        invariant_sublists = split_by_key(cluster, invariant)
        partitioned_clusters.extend(invariant_sublists)
    return partitioned_clusters


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


def load_reactioncenters_from_path(graphs_filename, verbose=True):
    if verbose:
        print("Loading data...")

    with open(graphs_filename, 'rb') as f:
        reactions = pickle.load(f)

    if verbose:
        print("Data loaded.")
        print("Computing reaction centers...")

    reaction_centers = []

    # Initialize tqdm progress bar
    for reaction in tqdm(reactions, desc="Processing Reactions", unit="reaction"):
        reaction_centers.append(get_rc(reaction['ITS']))

    if verbose:
        print("Reaction centers computed.")

    return reaction_centers


def load_reaction_centers(dataset='small', verbose=True):
    if dataset == 'small':
        graphs_filename = 'Data/ITS_graphs_100_subset.pkl'
        verbose = False
    elif dataset == 'medium':
        graphs_filename = 'Data/ITS_graphs.pkl.gz'
    elif dataset == 'large':
        graphs_filename = 'Data/ITS_largerdataset.pkl.gz'
    else:
        graphs_filename = 'Data/ITS_graphs_100_subset.pkl'

    return load_reactioncenters_from_path(graphs_filename, verbose)


def run_pipeline(pipeline_title, reaction_centers, invariants, iso=True):
    clusters = [(0, reaction_centers)]
    print(f"===== '{pipeline_title}' =====")

    prev_num_clusters = len(clusters)
    start_time = 0
    end_time = 0

    def print_stats():
        print(f" - Time: {end_time - start_time:.2f} s")
        print(f" - Clusters: {len(clusters)} (+{len(clusters) - prev_num_clusters})")

    total_start_time = time.time()
    for invariant in invariants:
        start_time = time.time()
        clusters = partition_clusters_by_invariant(clusters, invariant)
        end_time = time.time()

        print(invariant.__name__)
        print_stats()

        prev_num_clusters = len(clusters)

    if iso:
        start_time = time.time()
        clusters = list(more_itertools.flatten(
            list(map(lambda cluster: split_by_equality(cluster, is_isomorphic), clusters))))
        end_time = time.time()
        print("isomorphism")
        print_stats()

    total_end_time = time.time()

    print(f"Total Time: {total_end_time - total_start_time:.2f} s")

    return clusters
