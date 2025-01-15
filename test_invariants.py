import time
from sys import argv

import invariants as inv
from utils import run_pipeline, load_rcs, split_by_equality, is_isomorphic
from weisfeiler_lehmann import wl_step, hash_graph, wl_init

reaction_centers = load_rcs(dataset=argv[1], l=0, verbose=True)


def clustering_score(clusters: list[list]):
    return sum(x * x for x in map(len, clusters))


def test(title, steps, iso=False):
    clusters = run_pipeline(title, reaction_centers, steps=steps, iso=iso)
    score = clustering_score(clusters)
    print(f"Clusters: {len(clusters)}")
    print(f"Sum of Squares: {score:.2e}")

    if not iso:
        start_time = time.time()
        for cluster in clusters:
            split_by_equality(cluster, is_isomorphic)
        end_time = time.time()
        print(f"Iso Time: {end_time - start_time:.2f} s")


test(title="Number of Nodes", steps=[inv.number_of_nodes])
test(title="Number of Edges", steps=[inv.number_of_edges])
test(title="Degree Distribution", steps=[inv.degree_distribution])
test(title="Elemental Composition", steps=[inv.elemental_composition])
test(title="Bond Type Distribution", steps=[inv.bond_type_distribution])
test(title="Clustering Coefficients", steps=[inv.clustering_coefficients])
test(title="WL (1)", steps=[(wl_init, hash_graph)])
test(title="WL (2)", steps=[(wl_init, hash_graph), (wl_step, hash_graph)])
test(title="Isomorphism", steps=[], iso=True)
