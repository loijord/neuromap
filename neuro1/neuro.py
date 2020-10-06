from neuromap import InteractiveGraph
import numpy as np
import matplotlib.pyplot as plt
import networkx as nx
from matplotlib import rc
rc('text', usetex=True)

nodes = np.array(['A', 'B', 'C', 'D', 'E', 'F', 'G', 'R', 'S', 'H', 'F - E', 'A - B', 'C - D', 'F - H', 'H - C - D', 'B - C'])
edges = np.array([('A', 'B'), ('B', 'C'), ('C', 'D'), ('E', 'A - B'), ('F', 'E'), ('F', 'H'), ('F', 'B - C'), ('G', 'F - E'), ('R', 'F - H'), ('S', 'H - C - D'), ('H', 'C - D')])
pos = np.array([[-3.312971323362506, 2.8740904485585332], [-2.6027390350324096, -2.313346228239845], [3.022623521400287, -2.254398084185318], [3.644076773689121, 2.785668232476743], [-2.005498247118465, 1.6951275674679929], [-0.24605916920981663, 0.6340609744865064], [-0.6173169562914582, 2.6530349083540576], [0.2624025826628662, 2.829879340517638], [1.949204267446845, -0.7217463387676153], [1.3519634795329, 1.3856498111817261], [-0.7182022245201649, 1.2235424150317766], [-2.9820676435723477, 0.3245832182002397], [3.3454563797321475, 0.19194989407755347], [1.247042800575045, 1.2898590770931198], [2.7240031274433134, 1.017223910840932], [0.20994224318393861, -2.283872156212581]])
midpos = np.array([('A', 'B'), ('B', 'C'), ('C', 'D'), ('F', 'E'), ('F', 'H'), ('H', 'C - D')])
sizes = [500, 6500, 9500, 500, 500, 500, 500, 1000, 1000, 1000, 500, 500, 500, 500, 500, 500]
labels = ['$(a^n)^m$', 'B', 'C', '$a^{nm}$', 'E', 'F', r"$\left [\begin{array}{c}n\to m\\a\to a^n\end{array}\right.$", r"$n \to nm$", '$nm$ yra langeliu kiekis \n stačiakampyje su kraštinėmis n ir m', 'H']
images = {'B': 'power_defappl.png', 'C': 'power_permute.png', 'E': 'power_def_apply_process.png', 'F': 'power_def.png', 'H': 'powerdef_nm.png'}
imsizes = {'B': 0.15, 'C': 0.2, 'E': 0.2, 'F': 0.2, 'H': 0.2}

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