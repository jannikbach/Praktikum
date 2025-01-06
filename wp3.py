import pickle
import more_itertools
import networkx as nx
import time

from utils import is_isomorphic, split_by_equality,split_by_key, get_rc

VERBOSE = True

print("Loading data...")
with open('Data/ITS_graphs.pkl.gz', 'rb') as f:
    reactions = pickle.load(f)
print("Data loaded.")

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

def number_of_nodes(reaction):
    return reaction.number_of_nodes()

def number_of_edges(reaction):
    return reaction.number_of_edges()
def degree_distribution(reaction):
    return sorted([d for _, d in reaction.degree()])

def elemental_composition(reaction):
    element_counts = {}
    for _, data in reaction.nodes(data=True):
        element = data.get('element', None)
        if element:
            element_counts[element] = element_counts.get(element, 0) + 1
    return tuple(sorted(element_counts.items()))

def bond_type_distribution(reaction):
    bond_counts = {}
    for _, _, data in reaction.edges(data=True):
        bond_order = data.get('order', None)
        if bond_order:
            bond_counts[bond_order] = bond_counts.get(bond_order, 0) + 1
    return tuple(sorted(bond_counts.items()))

def clustering_coefficients(reaction):
    return tuple(sorted(nx.clustering(reaction).values()))

def cycle_basis(reaction):
    return tuple(sorted([tuple(sorted(cycle)) for cycle in nx.cycle_basis(reaction)]))

def partition_clusters_by_invariant(clusters, invariant):
    """
    Partition clusters by invariant
    """
    partitioned_clusters = [[]]
    for cluster in clusters:
        invariant_sublists = split_by_key(cluster, invariant)
        partitioned_clusters.extend(invariant_sublists)
    return partitioned_clusters

i = 0
reaction_centers = []
for reaction in reactions:
    i += 1
    if VERBOSE and i % 1000 == 0:
        print(f"{(i / len(reactions)) * 100:.2f}%")
    reaction_centers.append(get_rc(reaction['ITS']))

clusters = [reaction_centers]
start_time = time.time()
clusters = partition_clusters_by_invariant(clusters, number_of_nodes)
print("num clusters1:", len(clusters))
clusters = partition_clusters_by_invariant(clusters, number_of_edges)
print("num clusters1:", len(clusters))
clusters = partition_clusters_by_invariant(clusters, degree_distribution)
print("num clusters3:", len(clusters))
clusters = partition_clusters_by_invariant(clusters, elemental_composition)
print("num clusters4:", len(clusters))
clusters = partition_clusters_by_invariant(clusters, bond_type_distribution)
print("num clusters5:", len(clusters))
clusters = partition_clusters_by_invariant(clusters, clustering_coefficients)
print("num clusters6:", len(clusters))
clusters = list(more_itertools.flatten(list(map(lambda cluster: split_by_equality(cluster, is_isomorphic), clusters))))
end_time = time.time()


print("num clusters:", len(clusters))
execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
