import invariants as inv
from utils import run_pipeline, load_rcs

reaction_centers = load_rcs('Data/ITS_graphs.pkl.gz')

run_pipeline("Way too big", reaction_centers, [
    inv.number_of_nodes,
    inv.number_of_edges,
    inv.degree_distribution,
    inv.elemental_composition,
    inv.bond_type_distribution,
    inv.clustering_coefficients,
])

run_pipeline("Simple but efficient", reaction_centers, [
    inv.elemental_composition,
])
