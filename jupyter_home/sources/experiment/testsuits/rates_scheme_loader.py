import json

from os import listdir
from os.path import join, exists, isdir

import matplotlib.pyplot as plt

import sources.experiment.testsuits.scheme_loader_functions as loadf
import sources.experiment.experiment_plotting as expplot


class RatesSchemeLoader:

    def __init__(self, directory: str):
        with open(directory + '/dataset_data.json', 'r') as fp:
            data = json.load(fp)

        schemes = {}

        s_matrix, exp_info = loadf.load_experiment_dir(join(directory, "standard_GA"), data["snapshot_count"])
        schemes["standard"] = {
            "experiment_matrix": s_matrix,
            "experiment_info": exp_info
        }

        rates_dir = join(directory, "immigrants_GAs")
        if exists(rates_dir):
            dirs = [d for d in listdir(rates_dir) if isdir(join(rates_dir, d)) and not d.startswith(".")]

            schemes["rates"] = []
            for d in dirs:
                i_matrix, exp_info = loadf.load_experiment_dir(join(rates_dir, d), data["snapshot_count"])

                schemes["rates"].append({
                    "experiment_matrix": i_matrix,
                    "experiment_info": exp_info
                })

            self.schemes = schemes
            self.data = data
        else:
            raise Exception("missing immigrants dir: {0}".format(rates_dir))

    def flatten_schemes(self, show_standard=True):
        if show_standard:
            schemes_list = [self.schemes["standard"]["experiment_matrix"]]
            schemes_names = ["standard"]
        else:
            schemes_list = []
            schemes_names = []

        info = self.schemes["standard"]["experiment_info"]

        rates_list = self.schemes["rates"]
        for exp_dict in rates_list:
            schemes_list.append(exp_dict["experiment_matrix"])
            schemes_names.append("{0: .2f}%".format(exp_dict["experiment_info"]["rate_random_immigrants"]))

        return schemes_list, schemes_names, info

    def save_best_median(self, img_path: str, show_standard=True):
        schemes_list, scheme_names, info = self.flatten_schemes(show_standard)

        expplot.best_vs_best_median_one_graph(img_path, schemes_list, scheme_names, self.data["snapshot_count"],
                                              info["num_generations"], "median best individual per generation")

    def save_max_generation_reach(self, img_path: str):
        schemes_list, scheme_names, info = self.flatten_schemes()

        f, axs = plt.subplot(1)
        expplot.plot_median_generation_porcent_reach(axs, schemes_list, self.data["snapshot_count"],
                                                     info["num_generations"], scheme_names,
                                                     "generation max value reach", "number_generation")

        plt.savefig(img_path)

