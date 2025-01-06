"""
Implements a simple clustering algorithm.
"""
import pickle
import time

from utils import is_isomorphic, split_by_equality, get_rc

print("Loading data...")
with open('Data/ITS_graphs.pkl.gz', 'rb') as f:
    reactions = pickle.load(f)
print("Data loaded.")

reactions = list(map(lambda g: get_rc(g['ITS']), reactions))

start_time = time.time()
clusters = split_by_equality(reactions, is_isomorphic)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
print("num reactions:", len(reactions))
print("num clusters:", len(clusters))
