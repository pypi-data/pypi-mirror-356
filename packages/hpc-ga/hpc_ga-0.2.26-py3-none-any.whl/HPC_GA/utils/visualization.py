import matplotlib.pyplot as plt
from ..core.genetic_algorithm import GeneticAlgorithm

def plot_evolution(ga: 'GeneticAlgorithm'):
    plt.plot(ga.history["best"], label="Best Fitness")
    plt.plot(ga.history["avg"], label="Average Fitness")
    plt.legend()
    plt.show()