import time
import pickle
from concurrent.futures import ProcessPoolExecutor
from itertools import groupby
from operator import itemgetter

import more_itertools
import networkx as nx
from tqdm import tqdm


def split_by_key(cluster, key_func):
    # Step 1: Decorate each element with its key
    decorated = [(key_func(item), item) for item in cluster]

    # Step 2: Sort the decorated list by key
    decorated.sort(key=itemgetter(0))

    # Step 3: Group by the precomputed key
    grouped = groupby(decorated, key=itemgetter(0))

    # Step 4: Extract the original items from each group
    return [[item for _, item in group] for _, group in grouped]


def split_by_equality(cluster, is_equal):
    buckets = []
    for graph in cluster:
        found_bucket = False
        for bucket in buckets:
            representative = bucket[0]
            if is_equal(graph, representative):
                bucket.append(graph)
                found_bucket = True
                break
        if not found_bucket:
            # spawn new cluster
            buckets.append([graph])

    return buckets


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


def get_rc(G: nx.Graph, ID=None) -> nx.Graph:
    # Extract edges with "standard_order" not equal to 0
    edges = [(e[0], e[1]) for e in G.edges(data=True) if e[2]["standard_order"] != 0]
    rc = nx.edge_subgraph(G, edges)
    rc = rc.copy()
    # Assign the parent identifier (R-id)
    rc.graph["ID"] = ID

    return rc


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


def _unflatten(graphs, cluster_sizes):
    graph_i = 0
    clusters = []
    for cluster_size in cluster_sizes:
        clusters.append(graphs[graph_i:graph_i + cluster_size])
        graph_i += cluster_size
    return clusters


def run_pipeline(pipeline_title, reaction_centers, steps, max_workers=1, iso=True):
    clusters = [reaction_centers]
    print(f"===== '{pipeline_title}' =====")

    prev_num_clusters = len(clusters)
    start_time = 0
    end_time = 0

    def print_stats():
        print(f" - Time: {end_time - start_time:.2f} s")
        print(f" - Clusters: {len(clusters)} (+{len(clusters) - prev_num_clusters})")

    total_start_time = time.time()
    for transformation, invariant in steps:
        start_time = time.time()

        cluster_sizes = [len(cluster) for cluster in clusters]

        # flatten
        all_graphs = list(more_itertools.flatten(clusters))

        # transform parallel
        with ProcessPoolExecutor(max_workers=max_workers) as executor:
            if transformation is not None:
                all_graphs = list(executor.map(transformation, all_graphs))
            labels = list(executor.map(invariant, all_graphs))
        decorated_graphs = list(zip(labels, all_graphs))

        # unflatten
        clusters_of_decorated_graphs = _unflatten(decorated_graphs, cluster_sizes)

        clusters = []
        for cluster_of_decorated_graphs in clusters_of_decorated_graphs:
            # Step 2: Sort the decorated list by key
            cluster_of_decorated_graphs.sort(key=itemgetter(0))

            # Step 3: Group by the precomputed key
            grouped = groupby(cluster_of_decorated_graphs, key=itemgetter(0))

            for _, group in grouped:
                cluster_of_undecorated_graphs = [item for _, item in group]
                clusters.append(cluster_of_undecorated_graphs)

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
