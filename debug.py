import pickle

import networkx as nx

from utils import is_isomorphic, split_by_equality, load_reaction_centers, run_pipeline
from weisfeiler_lehmann import wl_init, wl_step


def print_cluster_sizes(clusters):
    sizes = list(map(lambda c: len(c[1]), clusters))
    sizes.sort(reverse=True)
    print(len(clusters))
    print(sizes)
    print(sum(sizes))

    # histogram
    d = {}
    for size in sizes:
        if size not in d:
            d[size] = 1
        else:
            d[size] += 1
    print(d)


reaction_centers = load_reaction_centers("medium")

# print("=== raw iso split ===")
# iso_clusters = split_by_equality((0, reaction_centers), is_isomorphic)
# print("DONE")
# print("Isomorphism clusters:")
# print_cluster_sizes(iso_clusters)

wl_clusters = run_pipeline("custom wl", reaction_centers, [
    wl_init,
    wl_step
], iso=False)


def find_matches(graphs1, graphs2):
    matches = []
    for g1 in graphs1:
        for g2 in graphs2:
            if is_isomorphic(g1, g2):
                matches.append((cluster_a, cluster_b))
    return matches


duplicates: list[tuple[nx.Graph, nx.Graph]] = []
for i, cluster_a in enumerate(wl_clusters[:-1]):
    for cluster_b in wl_clusters[i + 1:]:
        # for each unique and different pair (cluster_a, cluster_b):
        pairs = find_matches(cluster_a, cluster_b)
        if pairs:
            duplicates.extend(pairs)

print("======================= DUPLICATES =======================")
print("num duplicates:", len(duplicates))
print("graph IDs:")
for a, b in duplicates:
    print((a, b))

exit()

print("======================= RAW ISO SPLIT =======================")
iso_clusters = split_by_equality((0, critical_rcs), is_isomorphic)
print("DONE")
print("Isomorphism clusters:")
print_cluster_sizes(iso_clusters)

print("======================= WL SPLIT =======================")
wl_clusters = run_pipeline("custom wl", critical_rcs, [
    wl_init,
], iso=False)
print_cluster_sizes(wl_clusters)

print("======================= WL STEP =======================")
wl_clusters = run_pipeline("custom wl", critical_rcs, [
    wl_init,
    wl_step,
], iso=False)
print_cluster_sizes(wl_clusters)
