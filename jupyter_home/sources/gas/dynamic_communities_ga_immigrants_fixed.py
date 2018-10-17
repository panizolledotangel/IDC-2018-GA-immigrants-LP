import math

from deap import base
from deap import creator
from deap import tools

import numpy as np

import sources.auxiliary_funtions as auxf
from sources.ga_skeleton import GaSkeleton
from sources.gas.dynamic_communities_ga_interface import DynamicCommunitiesGAInterface
from sources.gas.dynamic_ga_immigrants_config import DynamicGaImmigrantsConfiguration


class DynamicCommunitiesGAImmigrantsFixed(DynamicCommunitiesGAInterface):

    def __init__(self, snapshots: list, individual_sizes: list, statistics_dir: str,
                 config: DynamicGaImmigrantsConfiguration):

        super().__init__(snapshots, individual_sizes, statistics_dir)
        self.config = config

    def make_dict(self):
        return self.config.make_dict()

    def find_communities(self):

        snp_size = len(self.snapshots)
        snapshot_members = [None] * snp_size
        immigrants = [None] * snp_size
        repaired_list = [None] * snp_size

        generations_taken = [0]*snp_size

        best_pop = None
        for i in range(snp_size):
            print("working on snapshot {0}...".format(i))
            self.config.set_snapshot(i)
            g = self.snapshots[i]

            # Initialize GA
            toolbox = base.Toolbox()
            toolbox.register("individual", auxf.create_individual, container=creator.Individual, graph=g,
                             n=self.individual_sizes[i])
            toolbox.register("evaluate", auxf.evaluate_individual, graph=g)

            # immigrants tools
            reparator = self.config.get_reparator()
            reparator.set_snapshot(i)
            toolbox.register("repair", reparator.repair)

            if i is 0:
                n_gen_repaired = [0] * self.config.get_ga_config().population_size
                n_elite = 0
                n_random = self.config.get_ga_config().population_size
                pop_initial = [toolbox.individual() for i in range(self.config.get_ga_config().population_size)]

                # Evaluate the individuals
                fitnesses = toolbox.map(toolbox.evaluate, pop_initial)
                for ind, fit in zip(pop_initial, fitnesses):
                    ind.fitness.values = fit
            else:
                pop_initial, n_elite, n_random, n_gen_repaired = self._select_immigrants(toolbox, best_pop)

            toolbox.register("mate", tools.cxTwoPoint)
            toolbox.register("mutate", auxf.mutate_individual, graph=g,
                             probability=self.config.get_ga_config().mutation_rate)
            toolbox.register("select", tools.selTournament, tournsize=10)

            ga = GaSkeleton(pop_initial, toolbox, self.config.get_ga_config())

            best_pop, statistics = ga.start()

            # save statistics
            np.savetxt(self.statistics_dir + "/snapshot_{0}.csv".format(i), statistics, delimiter=",", fmt="%10.5f")
            generations_taken[i] = statistics.shape[0]

            # save immigrants
            immigrants[i] = [n_elite, n_random]
            repaired_list[i] = n_gen_repaired

            # save solution
            snapshot_members[i] = auxf.decode(tools.selBest(best_pop, 1)[0])

        r_data = {
            "snapshot_members": snapshot_members,
            "generations_taken": generations_taken,
            "immigrants": immigrants,
            "repaired_list": repaired_list
        }
        return r_data

    def _select_immigrants(self, tbox, past_population):
        num_elite_immigrants = int(math.ceil((1 - self.config.get_rate_random_immigrants()) *
                                             self.config.get_ga_config().population_size))

        num_random_immigrants = int(math.ceil(self.config.get_rate_random_immigrants() *
                                              self.config.get_ga_config().population_size))

        if num_elite_immigrants > 0:
            elite_immigrants = list(tbox.map(tbox.clone, tools.selBest(past_population, num_elite_immigrants)))
            repaired_output = [tbox.repair(individual=x) for x in elite_immigrants]

            elite_immigrants, n_gen_repaired = zip(*repaired_output)
            elite_immigrants = list(elite_immigrants)

            invalid_ind = [ind for ind in elite_immigrants if not ind.fitness.valid]
            fitnesses = tbox.map(tbox.evaluate, invalid_ind)
            for ind, fit in zip(invalid_ind, fitnesses):
                ind.fitness.values = fit
        else:
            elite_immigrants = []
            n_gen_repaired = 0

        random_immigrants = [tbox.individual() for _ in range(num_random_immigrants)]
        fitnesses = tbox.map(tbox.evaluate, random_immigrants)
        for ind, fit in zip(random_immigrants, fitnesses):
            ind.fitness.values = fit

        immigrants = elite_immigrants + random_immigrants
        return immigrants, num_elite_immigrants, num_random_immigrants, n_gen_repaired
