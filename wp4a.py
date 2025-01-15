import sys

from invariants import wl_with_iterations
from utils import run_pipeline, load_rcs

if __name__ == "__main__":
    if len(sys.argv) < 2:
        reaction_centers = load_rcs()
    else:
        reaction_centers = load_rcs(sys.argv[1])
    run_pipeline("WL it=1", reaction_centers, [
        (None, wl_with_iterations(1))
    ])
    run_pipeline("WL it=3", reaction_centers, [
        (None, wl_with_iterations(7))
    ])
