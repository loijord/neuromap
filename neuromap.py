# https://stackoverflow.com/a/63838446/3044825
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import numpy as np
import scipy.spatial

class InteractiveGraph:
    def __init__(self, G):
        self.G = G
        self.node_clicked = False
        self.node_dblclicked = False
        self.xydata = None
        self.nodes = None
        self.sizes = {n:500 for n in self.G.nodes}
        self.mid_nodes = ()
        self.Nkdtree = None
        self.update_nodes()
        self.labels = list(range(len(self.G.nodes)))
        self.images = None
        self.imsizes = None
        self.pygments = None
        self.displaymode = False


        fig, ax = plt.subplots()
        self.cid1 = fig.canvas.mpl_connect('button_press_event', lambda event: self.on_press(event))
        self.cid2 = fig.canvas.mpl_connect('motion_notify_event', lambda event: self.on_motion(event))
        self.cid3 = fig.canvas.mpl_connect('button_release_event', lambda event: self.on_release(event))
        self.cid4 = fig.canvas.mpl_connect('key_press_event', lambda event: self.on_key(event))
        fig.patch.set_facecolor('white')

    def update_nodes(self):
        #stores nodelist, coords, Nkdtree
        if len(self.G.nodes)>0:
            # store nodes and kdtree of their pos
            self.nodes, coords = zip(*nx.get_node_attributes(self.G.subgraph(self.G.nodes), 'pos').items())
            self.Nkdtree = scipy.spatial.KDTree(coords) #kdtree of nodes

    def update_midnodes(self, edgelist=(), delete_node=None):
        if delete_node is not None:
            delete_edge = tuple(delete_node.split(' - '))
        else:
            delete_edge = None
        nx.set_edge_attributes(self.G, dict.fromkeys(edgelist, 'True'), 'midpos') #adding new nodes

        try:
            edgedict = nx.get_edge_attributes(self.G, 'midpos')
            if delete_edge is not None:
                edgedict.pop(delete_edge)
            source, target = zip(*edgedict.keys())
        except ValueError:
            self.mid_nodes = ()
            self.Mkdtree = None
            return

        source_coords = np.asarray(list(self.G.nodes[n]['pos'] if 'pos' in self.G.nodes[n]
                                        else self.G.nodes[n]['midpos'] for n in source))
        target_coords = np.asarray(list(self.G.nodes[n]['pos'] if 'pos' in self.G.nodes[n]
                                        else self.G.nodes[n]['midpos'] for n in target))

        mid_coords = (source_coords + target_coords) / 2
        self.mid_nodes = tuple(f'{x} - {y}' for x,y in zip(source, target))
        self.G.add_nodes_from(self.mid_nodes) #creating anonymous nodes
        nx.set_node_attributes(self.G.subgraph(self.mid_nodes), dict(zip(self.mid_nodes, mid_coords)), 'midpos')
        nx.set_node_attributes(self.G.subgraph(self.mid_nodes), dict(zip(self.mid_nodes, [500 for n in mid_coords])), 'size')
        self.Mkdtree = scipy.spatial.KDTree(mid_coords)

    def display(self):
        plt.axis('on')
        trans = plt.gca().transData.transform
        trans2 = plt.gcf().transFigure.inverted().transform
        for n in self.G.nodes():
            if 'pos' in self.G.nodes[n] and n in self.images:
                im = mpimg.imread(self.images[n])
                imsize = self.imsizes[n]
                (x, y) = self.G.nodes[n]['pos']
                xx, yy = trans((x, y))  # figure coordinates
                xa, ya = trans2((xx, yy))  # axes coordinates
                a0, b0 = (-4, -4)
                a1, b1 = (4, 4)
                x0, y0 = tuple(trans2(tuple(trans((a0, b0)))))
                x1, y1 = tuple(trans2(tuple(trans((a1, b1)))))
                B = x1 - x0, y1 - y0
                a = plt.axes([xa - imsize / 2.0, ya - imsize / 2.0, imsize, imsize])
                imsize = 1
                a.imshow(im, extent=(
                x - B[0] * imsize / 2.0, x + B[0] * imsize / 2.0, y - B[0] * imsize / 2.0, y + B[0] * imsize / 2.0))
                plt.axis('off')

    def refresh(self, display_images=False):
        plt.clf()
        plt.axis((-4, 4, -4, 4))
        ax = plt.gca()

        if self.labels is not None:
            labels = dict(zip(self.G.nodes, self.labels))
        else:
            labels = self.labels

        #print({m:dict(fc=n, ec="black", boxstyle="square", lw=3) for n,m in zip(self.pygments, self.nodes)})
        nx.draw_networkx_labels(self.G.subgraph(self.nodes), pos = nx.get_node_attributes(self.G, 'pos'),
                                bbox = dict(fc='greenyellow', ec="black", boxstyle="square", lw=3),
                                labels = labels)

        nx.draw_networkx_labels(self.G.subgraph(self.mid_nodes), pos=nx.get_node_attributes(self.G, 'midpos'), font_size=4,
                                labels={n:' ' for n in self.mid_nodes}, bbox=dict(fc="yellow", ec="black", boxstyle="circle", lw=2))

        nx.draw_networkx_edges(self.G.subgraph(self.nodes + self.mid_nodes),
                               pos={**nx.get_node_attributes(self.G, 'pos'), **nx.get_node_attributes(self.G, 'midpos')},
                               width=3.0, alpha=0.8, arrowsize=20,
                               #node_size=1000,
                               node_size = list(nx.get_node_attributes(self.G.subgraph(self.nodes + self.mid_nodes), 'size').values()),
                               edge_color='darkblue')


        if display_images:
            self.display()
            plt.sca(ax)
        plt.axis((-4, 4, -4, 4))
        plt.axis('on')
        plt.tick_params(left=True, bottom=True, labelleft=True, labelbottom=True)

    def on_key(self, event):
        if 'hidden_node' in self.G.nodes:
            if event.key == 'right':
                self.G.nodes[self.hidden_st[-1]]['size'] -= 200
                self.refresh()
                event.canvas.draw()
            elif event.key == 'left':
                self.G.nodes[self.hidden_st[-1]]['size'] += 200
                self.refresh()
                event.canvas.draw()
        elif event.key == 'enter':
            if self.displaymode==False:
                self.refresh()
                self.display()
                event.canvas.draw()
                self.displaymode = True
                print('displaymode is turned on')
            else:
                self.refresh()
                event.canvas.draw()
                self.displaymode = False
                print('displaymode is turned off')
        elif event.key == 'shift':
            print('EXTRACTING DATA:')
            print(f'nodes = np.array({list(self.G.nodes)})')
            print(f'edges = np.array({list(self.G.edges)})')
            print(f'pos = np.array({np.asarray([self.G.nodes[n]["pos"] if "pos" in self.G.nodes[n] else self.G.nodes[n]["midpos"] for n in self.G.nodes()]).tolist()})')
            print(f'midpos = np.array({list(nx.get_edge_attributes(self.G, "midpos").keys())})')
            print(f'sizes = {list(nx.get_node_attributes(self.G.subgraph(self.nodes + self.mid_nodes), "size").values())}')
            print(f'labels = {list(self.labels)}')
            print(f'images = {self.images}')
            print(f'imsizes = {self.imsizes}')


    def on_press(self, event):
        if event.inaxes is not None:
            if 'hidden_node' in self.G.nodes:
                if event.button == 1:
                    self.G.remove_node('hidden_node')
                    self.update_nodes()
                    self.update_midnodes(edgelist=[self.hidden_st])
                    self.refresh()
                    event.canvas.draw()
                elif event.button == 3:
                    self.G.remove_node('hidden_node')
                    self.update_nodes()
                    self.hidden_st = None
                    self.update_midnodes()
                    self.refresh()
                    event.canvas.draw()
            if len(self.nodes) > 0:
                self.xydata = np.array([event.xdata, event.ydata])
                close_idx = self.Nkdtree.query_ball_point(self.xydata, np.sqrt(0.1))
                #in case close node (tagged as pos) is identified
                if len(close_idx):
                    i = close_idx[0]
                    if event.dblclick:
                        print('[event.dblclick + close node of pos] received:', end=' ')
                        if not(self.node_dblclicked):
                            self.node_dblclicked = self.nodes[i]
                            self.G.add_node('temporary_node')
                            self.G.add_edge(self.node_dblclicked, 'temporary_node')
                            self.G.nodes['temporary_node']['tempos'] = self.xydata
                            print('temporary_node added')
                    else:
                        if not(self.node_dblclicked):
                            if event.button == 1: # leftclick
                                self.node_clicked = self.nodes[i]
                            #elif event.button == 2: self.node_pressed = self.nodes[i]
                            elif event.button == 3:  # rightclick
                                self.G.remove_node(self.nodes[i])
                                del self.labels[-1]
                                self.refresh()
                        else:
                            #replaces temporary node with clicked one and draws an edge
                            self.node_dblclicked = False
                            pr = next(self.G.predecessors('temporary_node'))
                            self.G.add_edge(pr, self.nodes[i])
                            self.G.remove_node('temporary_node')
                            self.update_nodes()
                            self.update_midnodes()
                            self.refresh()
                            event.canvas.draw()
                # in case no close node (tagged as pos) is identified
                else:
                    if event.dblclick:
                        new_node = input('type_new_node: ')
                        self.labels.append(new_node)
                        print('input is accepted.')
                        self.G.add_node(new_node)
                        self.G.nodes[new_node]['pos'] = self.xydata
                        self.G.nodes[new_node]['size'] = 1000
                        self.refresh()
                        event.canvas.draw()
                    else:
                        if self.node_dblclicked:
                            Mclose_idx = self.Mkdtree.query_ball_point(self.xydata, np.sqrt(0.1))
                            if len(Mclose_idx):
                                i = Mclose_idx[0]
                                if event.button == 1:
                                    print('[event.click + close node of midpos] received:', end=' ')
                                    # replaces temporary node with clicked one and draws an edge
                                    self.node_dblclicked = False
                                    pr = next(self.G.predecessors('temporary_node'))
                                    self.G.add_edge(pr, self.mid_nodes[i])
                                    self.G.remove_node('temporary_node')
                                    self.update_nodes()
                                    self.update_midnodes()
                                    self.refresh()
                                    event.canvas.draw()
                        else:
                            if event.button == 3:
                                Mclose_idx = self.Mkdtree.query_ball_point(self.xydata, np.sqrt(0.1))
                                if len(Mclose_idx):
                                    i = Mclose_idx[0]
                                    rm= self.mid_nodes[i]
                                    self.mid_nodes = (self.mid_nodes[:i] + self.mid_nodes[i+1:])
                                    self.update_midnodes(delete_node=rm)
                                    self.refresh()
                                    event.canvas.draw()

    def on_motion(self, event):
        if event.inaxes is not None:
            new_xydata = np.array([event.xdata, event.ydata])
            if self.node_clicked:
                self.xydata += new_xydata - self.xydata
                self.G.nodes[self.node_clicked]['pos'] = self.xydata
                self.update_midnodes()
                self.refresh()
            elif self.node_dblclicked:
                self.xydata += new_xydata - self.xydata
                self.G.nodes['temporary_node']['tempos'] = self.xydata
                self.refresh()
                nx.draw_networkx_edges(self.G.subgraph([self.node_dblclicked, 'temporary_node']),
                                       pos={self.node_dblclicked: self.G.nodes[self.node_dblclicked]['pos'],
                                            'temporary_node': self.G.nodes['temporary_node']['tempos']},
                                       width=3.0, alpha=0.5, edge_color='green')
            else:
                source, target = zip(*self.G.edges)
                #assuming all the graph consists of whether 'pos' or 'midpos' tagged nodes
                source_coords = np.asarray(list(self.G.nodes[n]['pos'] if 'pos' in self.G.nodes[n]
                                                else self.G.nodes[n]['midpos'] for n in source))
                target_coords = np.asarray(list(self.G.nodes[n]['pos'] if 'pos' in self.G.nodes[n]
                                                else self.G.nodes[n]['midpos'] for n in target))

                mid_coords = (source_coords + target_coords) / 2
                hidden_kdtree = scipy.spatial.KDTree(mid_coords)
                close_idx = hidden_kdtree.query_ball_point(new_xydata, np.sqrt(0.1))
                if len(close_idx):
                    self.G.add_node('hidden_node')
                    #self.G.nodes['hidden_node']['hiddenpos'] = hidden_kdtree[close_idx[0]]
                    self.refresh()
                    self.hidden_pos = hidden_kdtree.data[close_idx[0]]
                    self.hidden_st = (source[close_idx[0]], target[close_idx[0]])
                    nx.draw_networkx_labels(self.G.subgraph(['hidden_node']),
                                            pos={'hidden_node': self.hidden_pos}, font_size=4,
                                            labels={'hidden_node': ' '},
                                            bbox=dict(fc="orange", ec="black", boxstyle="circle", lw=2))
                else:
                    if 'hidden_node' in self.G.nodes:
                        self.G.remove_node('hidden_node')
                        self.refresh()
            event.canvas.draw()

    def on_release(self, event):
        if not(self.node_dblclicked):
            self.node_clicked = False
            self.update_nodes()
            self.update_midnodes()
            self.refresh()
            event.canvas.draw()