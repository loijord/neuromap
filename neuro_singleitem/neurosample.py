from neuromap import InteractiveGraph
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx

nodes = np.array(['A'])
edges = np.array([])
pos = np.array([[-0.61, 2.24]])
midpos = []
sizes = [500]
from matplotlib import rc

rc('text', usetex=True)
rc('font', family='serif')

labels = [r"\begin{eqnarray*}R_L&= 0\\ V_2&= 1\\ I_2&= 2\end{eqnarray*}"]
images = {}
imsizes = {}

G = nx.DiGraph()
G.add_nodes_from(nodes)
G.add_edges_from(edges)
nx.set_node_attributes(G, dict(zip(G.nodes(), pos.astype(float))), 'pos')
nx.set_node_attributes(G, dict(zip(G.nodes(), sizes)), 'size')

IG = InteractiveGraph(G)
IG.update_nodes()
IG.update_midnodes()
IG.labels = labels
IG.sizes = {n: 500 for n in nodes}
IG.images = images
IG.imsizes = imsizes
IG.refresh()
plt.show()