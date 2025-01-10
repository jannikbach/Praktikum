import invariants as inv
from utils import run_pipeline, load_reaction_centers

reaction_centers = load_reaction_centers('Data/ITS_graphs.pkl.gz')

run_pipeline("Way too big", reaction_centers, [
    (None, inv.number_of_nodes),
    (None, inv.number_of_edges),
    (None, inv.degree_distribution),
    (None, inv.elemental_composition),
    (None, inv.bond_type_distribution),
    (None, inv.clustering_coefficients),
])

run_pipeline("Simple but efficient", reaction_centers, [
    (None, inv.elemental_composition),
])
