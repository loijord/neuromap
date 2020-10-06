from neuromap import InteractiveGraph
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

nodes = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G'])
edges = np.array([['A', 'B'], ['A', 'C'], ['B', 'D'], ['B', 'E'], ['C', 'F'], ['C', 'G']])
midpos = []
pos = np.array([[0, 0], [-2, 1], [2, 1], [-3, 2], [-1, 2], [1, 2], [3, 2]])
labels = [1, 4, 9, 16, 25, 36, 49]
sizes = [500, 500, 500, 500, 500, 500, 500]
pygments = {'A': 'red', 'C':'green'}
images = {'B': 'miku.png', 'E': 'iggraph.png'}
imsizes = {'B': 0.2, 'E': 0.1}

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.set_node_attributes(G, dict(zip(G.nodes(), pos.astype(float))), 'pos')
nx.set_node_attributes(G, dict(zip(G.nodes(), sizes)), 'size')

IG = InteractiveGraph(G)
IG.update_nodes()
IG.update_midnodes()
IG.labels = labels
IG.sizes = {x: y for x, y in zip(nodes, sizes)}
IG.pygments = ['lightblue' if n not in pygments else pygments[n] for n in nodes]
IG.images = images
IG.imsizes = imsizes
IG.refresh()
plt.show()