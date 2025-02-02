import time
import pickle
from collections import defaultdict
from itertools import groupby
from operator import itemgetter

import more_itertools
import networkx as nx
from tqdm import tqdm


def split_by_key(cluster, key_func):
    buckets = defaultdict(list)

    for graph in cluster:
        key = key_func(graph)
        buckets[key].append(graph)

    return list(buckets.values())


def split_by_equality(cluster, is_equal):
    buckets = defaultdict(list)

    for graph in cluster:
        found_representative = False
        for representative in buckets:
            if is_equal(graph, representative):
                buckets[representative].append(graph)
                found_representative = True
                break

        if not found_representative:
            buckets[graph].append(graph)

    return list(buckets.values())


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


def get_rc(G: nx.Graph, l, ID=None) -> nx.Graph:
    # Extract edges with "standard_order" not equal to 0
    edges = [(e[0], e[1]) for e in G.edges(data=True) if e[2]["standard_order"] != 0]
    rc = nx.edge_subgraph(G, edges)

    # Assign the parent identifier (R-id)
    rc.graph["ID"] = ID

    # ego_graph get adjacent nodes iteratively over reaction center nodes
    if l > 0:
        for node in rc.nodes:
            ego = nx.ego_graph(G, node, center=True, radius=l)
            rc = nx.compose(rc, ego)
    return rc


def load_reactions_from_path(graphs_filename, verbose=True):
    if verbose:
        print("Loading data...")

    with open(graphs_filename, 'rb') as f:
        reactions = pickle.load(f)

    if verbose:
        print("Data loaded.")

    return reactions


def compute_rcs(reactions, l=0):
    return [get_rc(reaction['ITS'], l)
            for reaction in tqdm(reactions, desc="Processing Reactions", unit="reaction")]


def path_from_dataset(dataset):
    if dataset == 'small':
        return 'Data/ITS_graphs_100_subset.pkl'
    elif dataset == 'medium':
        return 'Data/ITS_graphs.pkl.gz'
    elif dataset == 'large':
        return 'Data/ITS_largerdataset.pkl.gz'
    else:
        raise ValueError("dataset must be one of 'small', 'medium', or 'large'")


def load_rcs(dataset='small', l=0, verbose=True):
    graphs_filename = path_from_dataset(dataset)
    reactions = load_reactions_from_path(graphs_filename, verbose)
    return compute_rcs(reactions, l)


def load_reactions(dataset='small', verbose=True):
    graphs_filename = path_from_dataset(dataset)
    return load_reactions_from_path(graphs_filename, verbose)


def run_pipeline(pipeline_title, reaction_centers, steps, iso=True):
    """
    steps is a list of invariants or tuples (transformation, invariant).
    """
    clusters = [reaction_centers]
    print(f"===== '{pipeline_title}' =====")

    prev_num_clusters = len(clusters)
    start_time = 0
    end_time = 0

    def print_stats():
        print(f" - Time: {end_time - start_time:.2f} s")
        print(f" - Clusters: {len(clusters)} (+{len(clusters) - prev_num_clusters})")

    total_start_time = time.time()
    for step in steps:

        # split if step is a tuple
        if isinstance(step, tuple):
            transformation, invariant = step
        else:
            # only invariant given
            transformation = None
            invariant = step

        start_time = time.time()
        if transformation is not None:
            for cluster in clusters:
                for graph in cluster:
                    # in-place transformation
                    transformation(graph)
        clusters = partition_clusters_by_invariant(clusters, invariant)
        end_time = time.time()

        if transformation is None:
            print(invariant.__name__)
        else:
            print(f"{transformation.__name__} | {invariant.__name__}")
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
