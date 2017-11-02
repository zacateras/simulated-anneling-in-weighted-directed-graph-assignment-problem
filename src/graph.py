import networkx as nx
import matplotlib.pyplot as plt
import random

G = nx.complete_graph(5)
for (u, v, w) in G.edges(data=True):
    w['weight'] = random.random()

pos = nx.spring_layout(G)

# nodes
nx.draw_networkx_nodes(G, pos, node_size=700)

# edges
nx.draw_networkx_edges(G, pos, width=6)

# labels
nx.draw_networkx_labels(G, pos, font_size=20, font_family='sans-serif')

# edge labels
labels = nx.get_edge_attributes(G,'weight')
nx.draw_networkx_edge_labels(G,pos,edge_labels=labels)

plt.show()
