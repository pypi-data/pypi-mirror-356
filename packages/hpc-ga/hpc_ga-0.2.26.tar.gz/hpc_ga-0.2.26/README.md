# hpc_ga

`hpc_ga` est un framework modulaire et extensible pour le développement d’algorithmes génétiques (GA) en Python, avec prise en charge du parallélisme à grande échelle. Il a été conçu pour être indépendant du problème, facilitant ainsi son intégration dans divers contextes d'optimisation.

## 📌 Fonctionnalités principales

- Architecture modulaire avec des classes pour :
  - `Chromosome` : représentation de solutions
  - `Population` : gestion des populations
  - `Crossover` : opérateurs de croisement
  - `Mutation` : opérateurs de mutation
  - `Fitness` : évaluation des individus
- Intégration de plusieurs modèles de parallélisme :
  - **Modèle insulaire (Island Model)**
  - **Modèle maître-esclave**
  - **Modèle cellulaire**
- Implémentation distribuée avec [Ray](https://docs.ray.io/)
- Compatible avec les environnements HPC (cluster, cloud, Grid5000)
- Installation facile via `pip`

## 🚀 Installation

```bash
pip install hpc_ga
```

## Exemple d'utilisation
from hpc_ga.population import Population
from hpc_ga.island_model import IslandModel

population = Population(initial_individuals=...)
island_model = IslandModel(num_islands=4)
island_model.run(population)

## Structure du projet
