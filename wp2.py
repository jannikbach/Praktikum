"""
Implements a simple clustering algorithm.
"""
import pickle

import networkx as nx

from split import split_by_equality
from src.rc_extract import get_rc

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


def is_isomorphic(rc1, rc2):
    """
    Check if two reaction centers are isomorphic.
    """
    return nx.is_isomorphic(rc1, rc2, node_match=node_match, edge_match=edge_match)


clusters = split_by_equality(reactions, is_isomorphic, lambda x: get_rc(x['ITS']))

print("num reactions:", len(reactions))
print("num clusters:", len(clusters))
