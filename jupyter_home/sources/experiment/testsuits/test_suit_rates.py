import json

from os import makedirs
from os.path import join, exists

from sources.gloaders.loader_interface import LoaderInterface
from sources.gas.dynamic_ga_immigrants_config import DynamicGaImmigrantsConfiguration
from sources.gas.dynamic_communities_ga_immigrants_fixed import DynamicCommunitiesGAImmigrantsFixed as GAImmigrants
from sources.gas.dynamic_communities_ga_standard import DynamicCommunitiesGAStandard as GAStandard
from sources.gas.paralelle_experiment import ParalelleExperiment
from sources.experiment.testsuits.rates_scheme_loader import RatesSchemeLoader

from sources.experiment.testsuits.test_suit_interface import TestSuitInterface


class TestSuitRates(TestSuitInterface):

    def __init__(self, test_bench: LoaderInterface, config: DynamicGaImmigrantsConfiguration, output_dir: str,
                 experiment_name: str, num_iter: int, rates_list: list, ts_min=0, ts_max=-1):

        super().__init__(test_bench, output_dir, experiment_name, num_iter, ts_min, ts_max)
        self.config = config
        self.rates_list = rates_list

    def do_test_suit(self):

        experiment_directory = join(self.output_dir, self.experiment_name)
        if not exists(experiment_directory):
            makedirs(experiment_directory)

        snapshots = self.test_bench.get_snapshots(self.ts_min, self.ts_max)

        immmigrants_dir = join(experiment_directory, "immigrants_GAs")
        if not exists(immmigrants_dir):
            makedirs(immmigrants_dir)

        print("Doing immigrants experiments...")
        for rate in self.rates_list:
            print("Doing rate {0}...".format(rate))

            self.config.rate_random_immigrants = [rate]*len(snapshots)
            exp_rate_path = join(immmigrants_dir, "fixed_{0:.2f}".format(rate))

            immigrants_ga = GAImmigrants(snapshots, self.test_bench.n_nodes, "", self.config)
            experiment = ParalelleExperiment(exp_rate_path, self.num_iter, immigrants_ga)
            experiment.start_experiment()

            print("Done!")

        print("Doing standard experiment...")

        exp_std_path = join(experiment_directory, "standard_GA")
        standard_ga = GAStandard(snapshots, self.test_bench.n_nodes, "", self.config)
        experiment = ParalelleExperiment(exp_std_path, self.num_iter, standard_ga)
        experiment.start_experiment()

        print("Done!")
        dataset_f_path = join(experiment_directory, "dataset_data.json")
        with open(dataset_f_path, 'w') as fp:
            json.dump(self.test_bench.get_dataset_info(), fp)

    def get_test_suit_loader(self):
        return RatesSchemeLoader(join(self.output_dir, self.experiment_name))
