import math
import random
import time
import matplotlib.pyplot as plt
import networkx as nx

import solution


class CoolingScheme:
    """
    Abstract class of a Cooling Scheme.
    Provides the next temperature value based on the initial T_0 and iteration number i.
    """
    def step(self, t_0, i):
        pass


class CoolingSchemeExponential(CoolingScheme):
    """
    Exponential Cooling Scheme.
    Subsequent values are generated according to the T_n(i) = T_0 * a ^ i formula.
    Can be parametrized with a parameter.
    """
    def __init__(self, a):
        if a <= 0 or a >= 1:
            raise (Exception, 'A must be a number greater than zero and lower than 1.')

        self.A = a

    def step(self, t_0, i):
        return t_0 * math.pow(self.A, i)


class CoolingSchemeLinear(CoolingScheme):
    """
    Linear Cooling Scheme.
    Subsequent values are generated according to the T_n(i) = T_0 - a * i formula.
    Can be parametrized with a parameter.
    """
    def __init__(self, a):
        if a <= 0:
            raise (Exception, 'A must be a number greater than zero.')

        self.A = a

    def step(self, t_0, i):
        return t_0 - self.A * i


class CoolingSchemeLogarithmic(CoolingScheme):
    """
    Logarithmic Cooling Scheme.
    Subsequent values are generated according to the T_n(i) = c / log(i + d) formula.
    Can be parametrized with c and d parameters.
    """
    def __init__(self, c, d):
        if c <= 0:
            raise (Exception, 'C must be a number greater than zero.')

        self.C = c
        self.D = d

    def step(self, t_0, i):
        return self.C / math.log(i + self.D)


class SimulatedAnnealingParameters:
    """
    Parameters of Simulated Annealing algorithm:
    - t_max - maximum temperature
    - t_min - minimum temperature
    - k_t - number of neighbour solutions checked in each iteration
    - cooling_scheme - type of a cooling scheme - one of Exponential, Logarithmic, Linear
    - i_s2_observation_interval - interval of generating observations (expressed in number of neighbour solution checked)
    - i_s3_observation_interval - interval of generating observations (expressed in number of temperature updates)
    """
    def __init__(self, t_max, t_min, k_t, cooling_scheme: CoolingScheme, i_s2_observation_interval=None, i_s3_observation_interval=None):
        self.T_max = t_max
        self.T_min = t_min
        self.k_t = k_t
        self.cooling_scheme = cooling_scheme
        self.i_s2_observation_interval = i_s2_observation_interval
        self.i_s3_observation_interval = i_s3_observation_interval


class SimulatedAnnealingObservation:
    """
    One observation of the simulation state:
    - category of an observation (identifier of a source)
    - current solution evaluation value
    - t - number of total iterations
    - i_s2 - total number of neighbour solution checks
    - i_s3 - total number of temperature updates
    """
    def __init__(self, category, evaluation, t, i_s2, i_s3):
        self.category = category
        self.evaluation = evaluation
        self.t = t
        self.i_s2 = i_s2
        self.i_s3 = i_s3


class SimulatedAnnealingResult:
    """
    Result of whole simulation:
    - best solution found
    - total time spend on simulation
    - generated observations

    The solution graph can be drawn using draw_solution method.
    Learning curve can be plotted using draw_observations_plot method.
    """
    def __init__(self, solution, total_time, observations, max_i_s2, max_i_s3):
        self.solution = solution
        self.total_time = total_time
        self.observations = observations
        self.max_i_s2 = max_i_s2
        self.max_i_s3 = max_i_s3

    def draw_solution(self):
        self.solution.draw()

    def draw_observations_plot(self):
        f, axarr = plt.subplots(1, 2)

        x_s3 = [obs.i_s3 for obs in filter(lambda x: x.category is 's3', self.observations)]
        y_s3 = [obs.evaluation for obs in filter(lambda x: x.category is 's3', self.observations)]
        axarr[0].plot(x_s3, y_s3)
        axarr[0].set_title('Each iteration')

        x_s2 = [obs.i_s2 for obs in filter(lambda x: x.category is 's2', self.observations)]
        y_s2 = [obs.evaluation for obs in filter(lambda x: x.category is 's2', self.observations)]
        axarr[1].plot(x_s2, y_s2)
        axarr[1].set_title('Each neighbour')

        plt.show()


class SimulatedAnnealing:
    """
    Simulated annealing algorithm.

    STEP 1.
        t = t_max
        choose random x_current
    STEP 2.
        choose x_next from x_current neighbourhood
        if eval(x_next) is better than eval(x_current) then x_current := x_next
        else if rand(0, 1) > e^(-d*eval/i) than

        repeat step 2. k_t times
    STEP 3.
        t = cooling_scheme(t)
        if t > t_min then goto step 2.
        else goto step 1.
    """
    @staticmethod
    def execute(
            nx_graph: nx.Graph,
            parameters: SimulatedAnnealingParameters,
            enable_status_printing: bool = False):

        observations = []

        start_time = time.time()

        # STEP 1
        T_0 = parameters.T_max
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

                # prevent overflows
                e_d = (next_est - crnt_est) / t

                if next_est < crnt_est:
                    crnt_s = next_s
                    crnt_est = next_est
                elif e_d < 709 and random.random() > math.exp(e_d):
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
                    break

            # STEP 3
            t = parameters.cooling_scheme.step(T_0, i_s3)

            if parameters.i_s3_observation_interval is not None and i_s3 % parameters.i_s3_observation_interval == 0:
                observations.append(
                    SimulatedAnnealingObservation(
                        's3',
                        crnt_est,
                        time.time() - start_time,
                        i_s2,
                        i_s3))

                if enable_status_printing:
                    print('s3: %s, t: %s' % (i_s3, t))

        end_time = time.time()
        total_time = end_time - start_time

        return SimulatedAnnealingResult(crnt_s, total_time, observations, i_s2, i_s3)
