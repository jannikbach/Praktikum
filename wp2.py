"""
Implements a simple clustering algorithm.
"""
import pickle
import networkx as nx
from src.rc_extract import get_rc

VERBOSE = False

print("Loading data...")
with open('Data/ITS_graphs_100_subset.pkl', 'rb') as f:
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

def is_isomorphic(rc1, rc2):
    """
    Check if two reaction centers are isomorphic.
    """
    return nx.is_isomorphic(rc1, rc2, node_match=node_match, edge_match=edge_match)

"""
each cluster is a tuple (reaction_center, reactions)
- reactions: a list of reactions from the original dataset
- reaction_center: the representative reaction center for this cluster
  (the reaction center of the first reaction in this list)
"""
clusters = []

i = 0
for reaction in reactions:
    i+=1
    if VERBOSE and i % 1000 == 0:
        print(f"{i}/{len(reactions)}")
    # get reaction center
    reaction_center = get_rc(reaction['ITS'])

    # find cluster to add this to
    found_cluster = False
    for cluster_reaction_center, cluster_reactions in clusters:
        if is_isomorphic(reaction_center, cluster_reaction_center):
            # add to existing cluster
            cluster_reactions.append(reaction)
            found_cluster = True
            break

    if not found_cluster:
        # spawn new cluster
        clusters.append((reaction_center, [reaction]))

print("num reactions: ", len(reactions))
print("num clusters:", len(clusters))