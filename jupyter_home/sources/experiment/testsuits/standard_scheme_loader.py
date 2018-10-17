import json

from os.path import join

import sources.experiment.testsuits.scheme_loader_functions as loadf
import sources.experiment.experiment_plotting as expplot


class StandardSchemeLoader:

    def __init__(self, directory: str):
        with open(directory + '/dataset_data.json', 'r') as fp:
            data = json.load(fp)

        schemes = {}

        s_matrix, exp_info = loadf.load_std_experiment_dir(join(directory, "standard_GA"), data["snapshot_count"])
        schemes["standard"] = {
            "experiment_matrix": s_matrix,
            "experiment_info": exp_info
        }
        self.schemes = schemes
        self.data = data

    def flatten_schemes(self):
        schemes_list = [self.schemes["standard"]["experiment_matrix"]]
        schemes_names = ["standard"]

        info = self.schemes["standard"]["experiment_info"]
        return schemes_list, schemes_names, info

    def save_best_median(self, img_path: str):
        schemes_list, scheme_names, info = self.flatten_schemes()

        expplot.best_vs_best_median_one_graph(img_path, schemes_list, scheme_names, self.data["snapshot_count"],
                                              "median best individual per generation")
