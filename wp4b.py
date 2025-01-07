from utils import load_reaction_centers, run_pipeline
from weisfeiler_lehmann import weisfeiler_lehmann_init, weisfeiler_lehmann_step, hash_graph

reaction_centers = load_reaction_centers('Data/ITS_graphs_100_subset.pkl')


def wl_init(graph) -> int:
    weisfeiler_lehmann_init(graph, node_attr=["element", "charge"], edge_attr=["order"])
    return hash_graph(graph)


def wl_step(graph) -> int:
    weisfeiler_lehmann_step(graph)
    return hash_graph(graph)


run_pipeline("WL it=3", reaction_centers, [
    wl_init,
    wl_step,
    wl_step,
    wl_step,
])
