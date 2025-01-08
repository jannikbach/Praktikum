import sys

from invariants import wl_with_iterations
from utils import load_reaction_centers, run_pipeline
from weisfeiler_lehmann import wl_init, wl_step, hash_graph

if __name__ == "__main__":
    if len(sys.argv) < 2:
        reaction_centers = load_reaction_centers()
    else:
        reaction_centers = load_reaction_centers(sys.argv[1])

    run_pipeline("custom WL", reaction_centers, [
        (wl_init, hash_graph),
        (wl_step, hash_graph),
        (wl_step, hash_graph),
    ], iso=False)
    run_pipeline("NX wl", reaction_centers, [
        (None, wl_with_iterations(3))
    ], iso=False)

