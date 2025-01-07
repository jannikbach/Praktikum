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

print("WL clusters:")
print_cluster_sizes(wl_clusters)


def clusters_match(cluster_a, cluster_b):
    _, rcs_a = cluster_a
    _, rcs_b = cluster_b
    if len(rcs_a) != len(rcs_b):
        return False
    # compare first graphs
    return is_isomorphic(rcs_a[0], rcs_b[0])


dingus = []
for cluster_a in wl_clusters:
    found_match = False
    for cluster_b in wl_clusters:
        if cluster_b == cluster_a: continue
        if clusters_match(cluster_a, cluster_b):
            found_match = True
            dingus.append(cluster_a)
    if not found_match:
        dingus.append(cluster_a)

print("======================= DINGUS =======================")
print_cluster_sizes(dingus)
# print(dingus)
