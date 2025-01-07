from invariants import wl_with_iterations
from utils import run_pipeline, load_reaction_centers

reaction_centers = load_reaction_centers('Data/ITS_graphs.pkl.gz')

run_pipeline("WL it=1", reaction_centers, [
    wl_with_iterations(1)
])
run_pipeline("WL it=7", reaction_centers, [
    wl_with_iterations(7)
])
