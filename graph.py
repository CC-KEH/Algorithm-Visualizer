import time
import networkx as nx
import matplotlib.pyplot as plt

from themes.colors import EDGE_COLOR, NODE_COLOR

class Graph_Visualizer:
    def __init__(self, is_directed=False, nodes=None, edges=None,is_random=False):
        self.is_directed = is_directed
        self.is_random = is_random
        self.nodes = nodes
        self.edges = edges

        if self.is_random:
            self.G = self.generate_random_connected_graph()
        else:
            if self.is_directed:
                self.G = nx.DiGraph()
            else:
                self.G = nx.Graph()

            if nodes:
                self.G.add_nodes_from(nodes)
            if edges:
                self.G.add_edges_from(edges)

    def generate_random_connected_graph(self):
        while True:
            G = nx.gnm_random_graph(n=self.nodes,m=self.edges,directed=self.is_directed)
            if nx.is_connected(G):
                return G

    def visualize_graph(self, pos):
        plt.figure()
        nx.draw(self.G, pos, with_labels=True)
        plt.show()
        time.sleep(0.5)

    # def visualize_search(self,pos):
    #     for i,node in enumerate(traverse_order,start=1):
    #         plt.clf()
    #         nx.draw(self.G,pos,with_labels=True,node_color=[NODE_COLOR if n==node else EDGE_COLOR for n in self.G.nodes])
    #         plt.pause(0.3)
    #     plt.show()
    #     time.sleep(0.5)


if __name__ == "__main__":
    # Example usage:
    # nodes = [1, 2, 3, 4]
    # edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    # pos = nx.spring_layout(nodes)  # Example layout

    # graph_visualizer = Graph_Visualizer(nodes=nodes, edges=edges)
    

    nodes = [1,2,3,4]
    edges = [(1, 2), (2, 3), (3, 4), (4, 1)]
    pos = nx.spring_layout(nodes)  # Example layout

    graph_visualizer = Graph_Visualizer(nodes=nodes, edges=edges)
    
    G = Graph_Visualizer(nodes=20,edges=20,is_random=True)
    G.visualize_graph(pos)