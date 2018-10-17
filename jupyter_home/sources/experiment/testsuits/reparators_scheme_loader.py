import json

from os import listdir
from os.path import join, exists, isdir
from typing import Dict

import numpy as np
import matplotlib.pyplot as plt
from scipy import stats

import sources.experiment.testsuits.scheme_loader_functions as loadf
import sources.experiment.experiment_plotting as expplot


class ReparatorsSchemeLoader:

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

            schemes["functions"] = []
            for d in dirs:
                i_matrix, exp_info = loadf.load_experiment_dir(join(rates_dir, d), data["snapshot_count"])
                repair_values = loadf.load_repaired_values(join(rates_dir, d))
                members_values = loadf.load_members_values(join(rates_dir, d), data["n_nodes"])

                schemes["functions"].append({
                    "repair_function": d,
                    "experiment_matrix": i_matrix,
                    "experiment_info": exp_info,
                    "repair_values": repair_values,
                    "members_values": members_values
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

        rates_list = self.schemes["functions"]
        for exp_dict in rates_list:
            schemes_list.append(exp_dict["experiment_matrix"])
            schemes_names.append(exp_dict["repair_function"])

        return schemes_list, schemes_names, info

    def save_best_median(self, img_path: str, img_name="save_best_median", show_standard=True):
        schemes_list, scheme_names, info = self.flatten_schemes(show_standard)

        expplot.best_vs_best_median_one_graph(join(img_path, img_name), schemes_list, scheme_names,
                                              self.data["snapshot_count"], "median best individual per generation")

    def save_best_median_min_max(self, img_path: str, repair_name: str):
        matrix = None

        i = 0
        functions_size = len(self.schemes["functions"])
        while i < functions_size and matrix is None:
            actual_scheme = self.schemes["functions"][i]
            if actual_scheme["repair_function"] == repair_name:
                matrix = actual_scheme["experiment_matrix"]
            i += 1

        expplot.max_min_median_best_generation(img_path,  matrix, self.schemes["standard"]["experiment_matrix"],
                                               self.data["snapshot_count"],
                                               "min, best and median fittest individual")

    def save_first_individual_improvement(self, img_path: str):
        schemes_list, scheme_names, info = self.flatten_schemes(False)
        standard_matrix = self.schemes["standard"]["experiment_matrix"]
        n_ts = self.data["snapshot_count"]

        f, axs = plt.subplots(1)
        expplot.plot_first_individual_improvement(axs, schemes_list, standard_matrix, scheme_names, n_ts,
                                                  "reparator efficiency", "fitness improvement")
        plt.savefig(img_path)

    def get_normalized_median_repair_values(self) -> Dict[str, np.array]:
        n_nodes = np.array(self.data["n_nodes"])

        norm_repair_values = {}
        for scheme in self.schemes["functions"]:
            repair_matrix = scheme["repair_values"]

            repair_matrix = np.median(repair_matrix, axis=[2, 0])
            repair_matrix = repair_matrix / n_nodes

            norm_repair_values[scheme["repair_function"]] = repair_matrix
        return norm_repair_values

    def get_mode_members(self) -> Dict[str, np.array]:
        members_values = {}
        for scheme in self.schemes["functions"]:
            members_list = scheme["members_values"]
            mode_members_ts = [list(stats.mode(members_ts)[0][0]) for members_ts in members_list]
            members_values[scheme["repair_function"]] = mode_members_ts

        return members_values
