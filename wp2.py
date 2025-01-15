"""
Implements a simple clustering algorithm.
"""
import pickle
import time

from utils import is_isomorphic, split_by_equality, get_rc, load_rcs


reaction_centers = load_rcs('medium')

cluster = (0, reaction_centers)

start_time = time.time()
clusters = split_by_equality(cluster, is_isomorphic)
end_time = time.time()

execution_time = end_time - start_time
print(f"Execution time: {execution_time:.2f} seconds")
print("num reactions:", len(reaction_centers))
print("num clusters:", len(clusters))
