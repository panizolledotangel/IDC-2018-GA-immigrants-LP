import json
import os
import datetime

from multiprocessing import Pool
from functools import partial

from sources.gas.dynamic_communities_ga_interface import DynamicCommunitiesGAInterface


def _pool_worker(n_iter, output_directory, dynamic_cooms_ga):
    print("Doing iteration {0}...".format(n_iter))

    s_iter_path = output_directory + "/iter_{0}".format(n_iter)
    if not os.path.exists(s_iter_path):
        os.makedirs(s_iter_path)

    dynamic_cooms_ga.statistics_dir = s_iter_path
    r_data = dynamic_cooms_ga.find_communities()

    with open(s_iter_path + '/execution_info.json', 'w') as fp:
        json.dump(r_data, fp)

    print("done!")


class ParalelleExperiment:

    def __init__(self, output_directory: str, num_iter: int, dynamic_cooms_ga: DynamicCommunitiesGAInterface):
        self.output_directory = output_directory
        self.num_iter = num_iter
        self.dynamic_cooms_ga = dynamic_cooms_ga
        self.number_processes = num_iter

    def start_experiment(self):
        init_date = datetime.datetime.now()
        iterations_params = [x for x in range(self.num_iter)]

        part_worker = partial(_pool_worker,
                              output_directory=self.output_directory,
                              dynamic_cooms_ga=self.dynamic_cooms_ga)

        with Pool(processes=self.number_processes) as pool:
            pool.map(part_worker, iterations_params)

        experiment_data = self.dynamic_cooms_ga.make_dict()
        experiment_data["init_date"] = str(init_date)
        experiment_data["end_date"] = str(datetime.datetime.now())
        experiment_data["iter_count"] = self.num_iter

        with open(self.output_directory + '/experiment_info.json', 'w') as fp:
            json.dump(experiment_data, fp)
