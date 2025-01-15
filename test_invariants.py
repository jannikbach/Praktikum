from sys import argv

import invariants as inv
from utils import run_pipeline, load_rcs

reaction_centers = load_rcs(dataset=argv[1], l=0, verbose=True)


def clustering_score(clusters: list[list]):
    return sum(x * x for x in map(len, clusters))


def test(title, steps, iso):
    clusters = run_pipeline(title, reaction_centers, steps=steps, iso=iso)
    score = clustering_score(clusters)
    print(f"{inv.__name__}")
    print(f"    Clusters: {len(clusters)}")
    print(f"    Sum of Squares: {score:.2e}")


invs = [
    inv.number_of_nodes,
    inv.number_of_edges,
    inv.degree_distribution,
    inv.elemental_composition,
    inv.bond_type_distribution,
    inv.clustering_coefficients,
]
for inv_ in invs:
    test(title=inv_.__name__, steps=[(None, inv_)], iso=False)

test(title="Ground Truth", steps=[], iso=True)
