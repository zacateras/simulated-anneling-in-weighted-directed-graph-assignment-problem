from src.graph import *
from src.simulated_annealing import *
import matplotlib.pyplot as plt

G = Graph.random_bipartite(100, 20, 0, 10)

# Graph.draw_bipartite(G)
# input("Press Enter to continue...")

parameters = SimulatedAnnealingParameters(
    t_max=100,
    t_min=0,
    k_t=1000,
    cooling_scheme=CoolingSchemeLinear(0.78),
    i_s2_observation_interval=100,
    i_s3_observation_interval=5
)

results = SimulatedAnnealing.execute(G, parameters)

# results['solution'].draw()

x = [obs.i_s2 for obs in results['observations']]
y = [obs.evaluation for obs in results['observations']]
plt.plot(x, y)
plt.show()
