import pickle
import time

import more_itertools

from invariants import number_of_nodes, number_of_edges, degree_distribution, elemental_composition, \
    bond_type_distribution, clustering_coefficients, partition_clusters_by_invariant
from utils import is_isomorphic, split_by_equality, get_rc

VERBOSE = True

print("Loading data...")
with open('Data/ITS_graphs.pkl.gz', 'rb') as f:
    reactions = pickle.load(f)
print("Data loaded.")

i = 0
reaction_centers = []
for reaction in reactions:
    i += 1
    if VERBOSE and i % 1000 == 0:
        print(f"{(i / len(reactions)) * 100:.2f}%")
    reaction_centers.append(get_rc(reaction['ITS']))


def run_pipeline(reaction_centers, invariants):
    clusters = [(0, reaction_centers)]
    print("===== RUNNING PIPELINE =====")

    prev_num_clusters = len(reaction_centers)
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

    start_time = time.time()
    clusters = list(more_itertools.flatten(
        list(map(lambda cluster: split_by_equality(cluster, is_isomorphic), clusters))))
    end_time = time.time()
    print("isomorphism")
    print_stats()

    total_end_time = time.time()

    print(f"Total Time: {total_end_time - total_start_time:.2f} s")

    return clusters

run_pipeline(reaction_centers, [
    number_of_nodes,
    number_of_edges,
    degree_distribution,
    elemental_composition,
    bond_type_distribution,
    clustering_coefficients,
])

run_pipeline(reaction_centers, [
    elemental_composition,
])