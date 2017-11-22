import random
import sys
import networkx as nx
import copy

from src import graph


class Solution:
    def __init__(self, nx_graph: nx.Graph):
        self.nxGraph = nx_graph

        if not nx.is_bipartite(nx_graph):
            raise (Exception, 'Provided graph must be bipartite.')

        part_1, part_2 = nx.bipartite.sets(nx_graph)
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
        estimate = 0.0
        for i in range(0, self.l_part_len):
            estimate += self.__get_weight(self.l_part[i], self.solution[i])
        return estimate

    def get_neighbour(self):
        neighbour = copy.copy(self)

        neighbour.solution = copy.deepcopy(self.solution)
        neighbour.remaining = copy.deepcopy(self.remaining)

        neighbour.__change_edge_random()

        return neighbour

    def draw(self):
        graph.Graph.draw_bipartite(self.nxGraph, list(zip(self.l_part, self.solution)))

    def __get_weight(self, v_1, v_2):
        if self.nxGraph.has_edge(v_1, v_2) and 'weight' in self.nxGraph[v_1][v_2]:
            return self.nxGraph[v_1][v_2]['weight']
        else:
            return sys.maxsize

    def __change_edge_random(self):
        idx_1, idx_2 = random.sample(range(0, self.g_part_len - 1), 2)
        self.__change_edge(idx_1, idx_2)

    def __change_edge(self, idx_1, idx_2):
        if idx_1 > self.g_part_len:
            raise (Exception, 'Index 1 must be lower than the number of vertices in greater bipartite.')

        if idx_2 > self.g_part_len:
            raise (Exception, 'Index 2 must be lower than the number of vertices in greater bipartite.')

        v_1 = self.solution[idx_1] if idx_1 < self.l_part_len else self.remaining[idx_1 - self.l_part_len]
        v_2 = self.solution[idx_2] if idx_2 < self.l_part_len else self.remaining[idx_2 - self.l_part_len]

        if idx_2 < self.l_part_len:
            self.solution[idx_2] = v_1
        else:
            self.remaining[idx_2 - self.l_part_len] = v_1

        if idx_1 < self.l_part_len:
            self.solution[idx_1] = v_2
        else:
            self.remaining[idx_1 - self.l_part_len] = v_2
