import random
import time
import math
import networkx as nx
from src import solution


class CoolingScheme:
    def step(self, t_0, i):
        pass


class CoolingSchemeExponential(CoolingScheme):
    def __init__(self, a):
        self.A = a

    def step(self, t_0, i):
        return t_0 * math.ldexp(self.A, i)


class CoolingSchemeLinear(CoolingScheme):
    def __init__(self, a):
        if a <= 0:
            raise (Exception, 'A must be a number greater than zero.')

        self.A = a

    def step(self, t_0, i):
        return t_0 - self.A * i


class CoolingSchemeLogarithmic(CoolingScheme):
    def __init__(self, c, d):
        self.C = c
        self.D = d

    def step(self, t_0, i):
        return self.C / math.log(i + self.D)


class SimulatedAnnealingParameters:
    def __init__(self, t_max, t_min, k_t, cooling_scheme: CoolingScheme, i_s2_observation_interval=None, i_s3_observation_interval=None):
        self.T_max = t_max
        self.T_min = t_min
        self.k_t = k_t
        self.cooling_scheme = cooling_scheme
        self.i_s2_observation_interval = i_s2_observation_interval
        self.i_s3_observation_interval = i_s3_observation_interval


class SimulatedAnnealingObservation:
    def __init__(self, category, evaluation, t, i_s2, i_s3):
        self.category = category
        self.evaluation = evaluation
        self.t = t
        self.i_s2 = i_s2
        self.i_s3 = i_s3


class SimulatedAnnealing:
    @staticmethod
    def execute(
            nx_graph: nx.Graph,
            parameters: SimulatedAnnealingParameters):

        observations = []

        start_time = time.time()

        # STEP 1
        t = parameters.T_max
        i_s2 = 0
        i_s3 = 0
        crnt_s = solution.Solution(nx_graph)
        crnt_est = crnt_s.get_estimate()

        while t > parameters.T_min:
            i_s3 += 1

            # STEP 2
            while True:
                i_s2 += 1

                next_s = crnt_s.get_neighbour()
                next_est = next_s.get_estimate()

                if next_est < crnt_est:
                    crnt_s = next_s
                    crnt_est = next_est
                elif random.random() > math.exp((next_est - crnt_est) / t):
                    crnt_s = next_s
                    crnt_est = next_est

                if parameters.i_s2_observation_interval is not None and i_s2 % parameters.i_s2_observation_interval == 0:
                    observations.append(
                        SimulatedAnnealingObservation(
                            's2',
                            crnt_est,
                            time.time() - start_time,
                            i_s2,
                            i_s3))

                if i_s2 % parameters.k_t == 0:
                    break;

            # STEP 3
            t = parameters.cooling_scheme.step(t, i_s3)

            if parameters.i_s3_observation_interval is not None and i_s3 % parameters.i_s3_observation_interval == 0:
                observations.append(
                    SimulatedAnnealingObservation(
                        's3',
                        crnt_est,
                        time.time() - start_time,
                        i_s2,
                        i_s3))

        end_time = time.time()
        total_time = end_time - start_time

        return {'solution': crnt_s, 'total_time': total_time, 'observations': observations}
