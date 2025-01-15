import sys

from invariants import wl_with_iterations
from utils import run_pipeline, load_reactions, compute_rcs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        reactions = load_reactions()
    else:
        reactions = load_reactions(sys.argv[1])

    for l in range(4):
        reaction_centers = compute_rcs(reactions, l)

        run_pipeline(f"NX wl L={l}", reaction_centers, [
            (None, wl_with_iterations(3))
        ], iso=False)
