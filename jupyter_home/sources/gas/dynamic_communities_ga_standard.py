from deap import base
from deap import creator
from deap import tools

import numpy as np

import sources.auxiliary_funtions as auxf
from sources.ga_skeleton import GaSkeleton
from sources.gas.dynamic_communities_ga_interface import DynamicCommunitiesGAInterface
from sources.gas.dynamic_ga_configuration import DynamicGaConfiguration


class DynamicCommunitiesGAStandard(DynamicCommunitiesGAInterface):

    def __init__(self, snapshots: list, individual_sizes: list, statistics_dir: str, config: DynamicGaConfiguration):
        super().__init__(snapshots, individual_sizes, statistics_dir)
        self.config = config

    def make_dict(self):
        return self.config.make_dict()

    def find_communities(self):
        snp_size = len(self.snapshots)
        snapshot_members = [None] * snp_size

        generations_taken = [0]*snp_size

        for i in range(snp_size):
            self.config.set_snapshot(i)
            g = self.snapshots[i]

            # Initialize GA
            toolbox = base.Toolbox()
            toolbox.register("individual", auxf.create_individual, container=creator.Individual, graph=g,
                             n=self.individual_sizes[i])

            toolbox.register("mate", tools.cxTwoPoint)
            toolbox.register("mutate", auxf.mutate_individual, graph=g, probability=self.config.get_ga_config().mutation_rate)
            toolbox.register("select", tools.selTournament, tournsize=10)
            toolbox.register("evaluate", auxf.evaluate_individual, graph=g)

            pop_initial = [toolbox.individual() for i in range(self.config.get_ga_config().population_size)]

            # Evaluate the individuals
            fitnesses = toolbox.map(toolbox.evaluate, pop_initial)
            for ind, fit in zip(pop_initial, fitnesses):
                ind.fitness.values = fit

            print("working on snapshot {0}...".format(i))
            ga = GaSkeleton(pop_initial, toolbox, self.config.get_ga_config())

            best_pop, statistics = ga.start()

            # save statistics
            np.savetxt(self.statistics_dir + "/snapshot_{0}.csv".format(i), statistics, delimiter=",", fmt="%10.5f")
            generations_taken[i] = statistics.shape[0]

            # save solution
            snapshot_members[i] = auxf.decode(tools.selBest(best_pop, 1)[0])

        r_data = {
            "snapshot_members": snapshot_members,
            "generations_taken": generations_taken
        }
        return r_data
