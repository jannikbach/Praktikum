"""
Implements a simple clustering algorithm.
"""
import pickle

from src.rc_extract import get_rc
from utils import is_isomorphic, split_by_equality

print("Loading data...")
with open('Data/ITS_graphs_100_subset.pkl', 'rb') as f:
    reactions = pickle.load(f)
print("Data loaded.")

clusters = split_by_equality(reactions, is_isomorphic, lambda x: get_rc(x['ITS']))

print("num reactions:", len(reactions))
print("num clusters:", len(clusters))
