import random

from deap import base
from deap import tools

import numpy as np

from sources.ga_config import GaConfiguration


class GaSkeleton:

    def __init__(self, population: list, toolbox: base.Toolbox, config: GaConfiguration):

        self.population = population
        self.toolbox = toolbox
        self.population_size = len(population)

        self.config = config

    def start(self):
        # copy of the population
        pop = list(self.population)

        statistics = []

        generation = 0
        convergence = False
        while not convergence and generation < self.config.number_generations:

            # Log the fitness values of the generation
            statistics.append(np.sort(np.array([i.fitness.values for i in pop])))

            # Elitism - select elite
            elite = tools.selBest(pop, int(self.config.elitism * self.population_size))
            elite = list(map(self.toolbox.clone, elite))

            # Select the next generation individuals
            offspring = self.toolbox.select(pop, self.config.offspring_size)
            # Clone the selected individuals
            offspring = list(map(self.toolbox.clone, offspring))

            # Apply crossover on the offspring
            for child1, child2 in zip(offspring[::2], offspring[1::2]):
                if random.random() < self.config.crossover_rate:
                    self.toolbox.mate(child1, child2)
                    del child1.fitness.values
                    del child2.fitness.values

            # Apply mutation on the offspring
            for mutant in offspring:
                if random.random() < self.config.mutation_rate:
                    self.toolbox.mutate(mutant)
                    del mutant.fitness.values

            # Evaluate the individuals with an invalid fitness
            invalid_ind = [ind for ind in offspring if not ind.fitness.valid]
            fitnesses = self.toolbox.map(self.toolbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit

            # Replace population with offsprings
            pop[:] = offspring

            # Elitism - Replace the K worst individuals by the elite
            worsts = tools.selWorst(pop, len(elite))
            for ind_replace in worsts:
                pop.remove(ind_replace)
            for ind in elite:
                pop.append(ind)

            # check for convergence
            if generation >= self.config.generations_to_converge:
                best_init = statistics[generation - self.config.generations_to_converge][-1]
                best_end = statistics[generation][-1]

                if abs(best_end - best_init) < self.config.threshold_converge:
                    convergence = True
            generation += 1

        statistics_matrix = np.zeros(len(statistics) * self.population_size).reshape(len(statistics), self.population_size)
        for i in range(len(statistics)):
            statistics_matrix[i, :] = statistics[i][:, 0]

        return pop, statistics_matrix
