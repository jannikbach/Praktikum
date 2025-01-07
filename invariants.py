from itertools import groupby

import networkx as nx

from utils import split_by_key


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


def iterate_weisfeiler(graph, iterations, node_attributes=None, edge_attr=None):
    if node_attributes is None:
        node_attributes = ['element', 'charge']
    if edge_attr is None:
        edge_attr = 'order'
    for node, data in graph.nodes(data=True):
        data['label'] = '_'.join([str(data.get(attr, None)) for attr in node_attributes])
    return nx.weisfeiler_lehman_graph_hash(graph, node_attr='label', edge_attr=edge_attr, iterations=iterations)


def wl_with_iterations(iters):
    def wl_iteration(clusters):
        return iterate_weisfeiler(clusters, iters)
    return wl_iteration

# Invatiant by: wl_with_iterations(7)



def partition_clusters_by_invariant(clusters, invariant):
    """
    Partition clusters by invariant
    """
    partitioned_clusters = []
    for cluster in clusters:
        invariant_sublists = split_by_key(cluster, invariant)
        partitioned_clusters.extend(invariant_sublists)
    return partitioned_clusters
