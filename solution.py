import copy
import random
import sys

import networkx as nx

import graph


class Solution:
    """
    Contains solution of the assignment problem.
    """
    def __init__(self, nx_graph: nx.Graph):
        self.nxGraph = nx_graph

        if not nx.is_bipartite(nx_graph):
            raise Exception('Provided graph must be bipartite.')

        part_1, part_2 = graph.Graph.sets_bipartite_nonconnected(nx_graph)
        part_1_len, part_2_len = len(part_1), len(part_2)

        if part_1_len < part_2_len:
            self.l_part, self.g_part = list(part_1), list(part_2)
            self.l_part_len, self.g_part_len = part_1_len, part_2_len
        else:
            self.l_part, self.g_part = list(part_2), list(part_1)
            self.l_part_len, self.g_part_len = part_2_len, part_1_len

        # initialize random solution
        self.solution = self.g_part[0:self.l_part_len]
        self.remaining = self.g_part[self.l_part_len:self.g_part_len]

    def get_estimate(self):
        """
        Returns value estimate of the solution.
        """
        estimate = 0.0
        for i in range(0, self.l_part_len):
            estimate += self.__get_weight(self.l_part[i], self.solution[i])
        return estimate

    def get_neighbour(self):
        """
        Returns a neighbour solution (with only one edge swapped).
        """
        neighbour = copy.copy(self)

        neighbour.solution = copy.deepcopy(self.solution)
        neighbour.remaining = copy.deepcopy(self.remaining)

        neighbour.__change_edge_random()

        return neighbour

    def draw(self):
        """
        Draws the solution.
        """
        graph.Graph.draw_bipartite(self.nxGraph, list(zip(self.l_part, self.solution)))

    def __get_weight(self, v_1, v_2):
        """
        Returns weight of the edge v_1:v_2.
        """
        if self.nxGraph.has_edge(v_1, v_2) and 'weight' in self.nxGraph[v_1][v_2]:
            return self.nxGraph[v_1][v_2]['weight']
        else:
            return sys.maxsize

    def __change_edge_random(self):
        """
        Randomly changes an edge in the solution.
        """
        idx_g = 0
        idx_l = 0
        while idx_g == idx_l:
            idx_g = random.randint(0, self.g_part_len - 1)
            idx_l = random.randint(0, self.l_part_len - 1)

        self.__change_edge(idx_g, idx_l)

    def __change_edge(self, idx_g, idx_l):
        """
        If vertices[idx_1] and vertices[idx_2] are connected then swaps its edges.
        If only one of them is connected than connecting edge is removed and vertices[idx_1]:vertices[idx_2] edge added.
        If both are disconnected then does not change edges state.
        """
        if idx_g > self.g_part_len:
            raise Exception('Index 1 must be lower than the number of vertices in greater bipartite.')

        if idx_l > self.l_part_len:
            raise Exception('Index 2 must be lower than the number of vertices in lesser bipartite.')

        v_g = self.solution[idx_g] if idx_g < self.l_part_len else self.remaining[idx_g - self.l_part_len]
        v_l = self.solution[idx_l]

        if idx_g < self.l_part_len:
            self.solution[idx_g] = v_l
            self.solution[idx_l] = v_g
        else:
            self.remaining[idx_g - self.l_part_len] = v_l
            self.solution[idx_l] = v_g
