import random

import matplotlib.pyplot as plt
import networkx as nx

import random_seed


class Graph:
    """
    Helper methods for networkx.Graph class.
    """
    @staticmethod
    def draw_bipartite(nx_graph: nx.Graph, vertex_tuples=None):
        """
        Draws bipartite either the provided weighted graph or the assignment solution if only vertex_tuples collection is provided.
        """
        if not nx.is_bipartite(nx_graph):
            raise (Exception, 'Provided graph must be bipartite.')

        l_part, r_part = nx.bipartite.sets(nx_graph)

        # position bipartite graph
        len_left = len(l_part)
        len_right = len(r_part)

        if len_left > len_right:
            add_left = (len_left - len_right) / 2
            add_right = 0
        else:
            add_left = 0
            add_right = (len_left - len_right) / 2

        pos = dict()

        pos.update((n, (1, i + add_left)) for i, n in enumerate(l_part))
        pos.update((n, (2, i + add_right)) for i, n in enumerate(r_part))

        # turn off axis off
        ax = plt.figure().gca()
        ax.set_axis_off()

        nx.draw_networkx_nodes(nx_graph, pos=pos)

        # thick edges
        if vertex_tuples is not None:
            nx.draw_networkx_edges(nx_graph, pos=pos, alpha=0.2)
            nx.draw_networkx_edges(nx_graph, pos=pos, edgelist=vertex_tuples, edge_color='b')
        else:
            nx.draw_networkx_edges(nx_graph, pos=pos)

        # edge labels
        labels = nx.get_edge_attributes(nx_graph, 'weight')
        nx.draw_networkx_edge_labels(nx_graph, pos=pos, edge_labels=labels)

        plt.show()

    @staticmethod
    def subgraph_edges(nx_graph: nx.Graph, vertex_tuples):
        """
        Returns subgraph of the provided graph containing only edges provided as vertex_tuples collection.
        """
        nx_subgraph = nx.empty_graph(len(nx_graph))

        for vertex_tuple in vertex_tuples:
            v_1, v_2 = vertex_tuple[0], vertex_tuple[1]

            if not nx_graph.has_edge(v_1, v_2) or 'weight' not in nx_graph[v_1][v_2]:
                raise (Exception, 'The edge is not present in the provided graph.')

            nx_subgraph.add_edge(vertex_tuple[0], vertex_tuple[1], weight=nx_graph[v_1][v_2]['weight'])

        return nx_subgraph

    @staticmethod
    def random_bipartite(n, m, w_min, w_max):
        """
        Generates random weighted bipartite graph:
        n - number of vertices in 'left' part
        m - number of vertices in 'right' part
        w_min - minimal weight generated
        w_max - maximal weight generated
        """
        nx_graph = nx.algorithms.bipartite.random_graph(n, m, random_seed.RANDOM_SEED)

        # add random weights
        for (_l, _r, data) in nx_graph.edges(data=True):
            data['weight'] = round((w_max - w_min) * random.random() + w_min, 2)

        return nx_graph
