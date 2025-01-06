"""
Implements a simple clustering algorithm.
"""
import pickle

import more_itertools
import networkx as nx

from utils import split_by_key, split_by_equality, is_isomorphic
from src.rc_extract import get_rc


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


def partition_clusters_by_invariant(clusters, invariant):
    """
    Partition clusters by invariant
    """
    partitioned_clusters = [[]]
    for cluster in clusters:
        #Split the list of reactions into lists, where the reactions are invariant under the same condition
        invariant_sublists = split_by_key(cluster, invariant)
        partitioned_clusters.extend(invariant_sublists)
    return partitioned_clusters

i=0
reaction_centers = []
for reaction in reactions:
    i+=1
    if VERBOSE and i % 1000 == 0:
        print(f"{(i / len(reactions)) * 100:.2f}%")
    # get reaction center
    reaction_centers.append(get_rc(reaction['ITS']))





clusters = [reaction_centers]
clusters = partition_clusters_by_invariant(clusters, number_of_nodes)
clusters = partition_clusters_by_invariant(clusters, number_of_edges)
clusters = list(more_itertools.flatten(list(map(lambda cluster: split_by_equality(cluster, is_isomorphic), clusters))))

print("num clusters:", len(clusters))


### reaction center
