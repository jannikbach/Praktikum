from utils import is_isomorphic, split_by_equality, load_reaction_centers, run_pipeline
from weisfeiler_lehmann import wl_init, wl_step

reaction_centers = load_reaction_centers("medium")
print("=== raw iso split ===")
iso_clusters = split_by_equality((0, reaction_centers), is_isomorphic)
print("DONE")

wl_clusters = run_pipeline("custom wl", reaction_centers, [
    wl_init,
    wl_step
], iso=False)

def print_cluster_sizes(clusters):
    sizes = list(map(len, clusters))
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

print("Isomorphism clusters:")
print_cluster_sizes(iso_clusters)
print("WL clusters:")
print_cluster_sizes(wl_clusters)