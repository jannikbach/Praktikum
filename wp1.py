import pickle

import networkx as nx

with open('Data/ITS_graphs_100_subset.pkl', 'rb') as f:
    data = pickle.load(f)

from utils import get_rc

# Call the function with the R-id of the graph as the parent
reaction_center = get_rc(data[1]['ITS'], ID=data[1]['R-id'])
print(reaction_center.graph.get("ID"))


nx.compose()

from synutility.SynVis.graph_visualizer import GraphVisualizer
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 1, figsize=(15, 10))
vis = GraphVisualizer()
vis.plot_its(data[1]['ITS'], ax[0], use_edge_color=True)
vis.plot_its(reaction_center, ax[1], use_edge_color=True)
plt.tight_layout()
plt.show()
