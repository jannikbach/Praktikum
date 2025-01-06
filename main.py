import pickle
import networkx as nx

with open('Data/ITS_graphs.pkl.gz', 'rb') as f:
    data = pickle.load(f)


from src.rc_extract import get_rc
reaction_center = get_rc(data[0]['ITS'])

from synutility.SynVis.graph_visualizer import GraphVisualizer
import matplotlib.pyplot as plt

fig, ax = plt.subplots(2, 1, figsize=(15, 10))
vis = GraphVisualizer()
vis.plot_its(data[0]['ITS'], ax[0], use_edge_color=True)
vis.plot_its(reaction_center, ax[1], use_edge_color=True)
plt.tight_layout()
plt.show()