import json
from os.path import join, isdir
from typing import List

import numpy as np


def load_ga(directory: str, num_snapshots: int, max_generations: int, size_population: int) -> np.array:
    snapshot_matrix = np.zeros(num_snapshots * max_generations * size_population)
    snapshot_matrix = snapshot_matrix.reshape(num_snapshots, max_generations, size_population)

    for i in range(num_snapshots):
        ss_i = np.loadtxt(join(directory, "snapshot_{0}.csv".format(i)), delimiter=",")
        actual_generations = ss_i.shape[0]
        ss_i = np.pad(ss_i, ((0, max_generations - actual_generations), (0, 0)), 'maximum')

        snapshot_matrix[i, :, :] = ss_i

    return snapshot_matrix


def load_ga_iterations(directory: str, num_iterations: int, num_snapshots: int, size_population: int):
    max_generations = load_generations_taken(directory, num_iterations)

    iter_matrix = np.zeros(num_iterations * num_snapshots * max_generations * size_population)
    iter_matrix = iter_matrix.reshape(num_iterations, num_snapshots, max_generations, size_population)

    for i in range(num_iterations):
        iter_dir = join(directory, "iter_{0}".format(i))

        if isdir(iter_dir):
            ss_i = load_ga(iter_dir, num_snapshots, max_generations, size_population)
            iter_matrix[i, :, :, :] = ss_i
        else:
            raise Exception("Missing directory: {0}".format(iter_dir))

    return iter_matrix


def load_generations_taken(directory: str, num_iterations: int):
    max_generations = 0
    for i in range(num_iterations):
        iter_dir = join(directory, "iter_{0}".format(i))
        with open(iter_dir + '/execution_info.json', 'r') as fp:
            exp_info = json.load(fp)
    
        num_generations = np.array(exp_info["generations_taken"])
        max_generations = max(max_generations, np.max(num_generations))
    return max_generations


def load_experiment_dir(directory: str, n_ts: int):
    with open(directory + '/experiment_info.json', 'r') as fp:
        exp_info = json.load(fp)

    info = exp_info["ga_configs"][0]
    info["n_snapshots"] = exp_info["n_snapshots"]
    info["reparators"] = exp_info["reparators"][0]
    info["iter_count"] = exp_info["iter_count"]
    info["rate_random_immigrants"] = exp_info["rate_random_immigrants"][0]

    standard_matrix = load_ga_iterations(directory, exp_info["iter_count"], n_ts, info["population_size"])
    return standard_matrix, info


def load_std_experiment_dir(directory: str, n_ts: int):
    with open(directory + '/experiment_info.json', 'r') as fp:
        exp_info = json.load(fp)

    info = exp_info["ga_configs"][0]
    info["n_snapshots"] = exp_info["n_snapshots"]
    info["iter_count"] = exp_info["iter_count"]

    standard_matrix = load_ga_iterations(directory, exp_info["iter_count"], n_ts, info["population_size"])
    return standard_matrix, info


def load_repaired_values(directory: str) -> np.array:
    with open(directory + '/experiment_info.json', 'r') as fp:
        exp_info = json.load(fp)

    n_iter = exp_info["iter_count"]
    n_snapshots = exp_info["n_snapshots"]
    ga_config = exp_info["ga_configs"]
    max_pop = ga_config[0]["population_size"]

    repair_matrix = np.zeros(n_iter*n_snapshots*max_pop).reshape(n_iter, n_snapshots, max_pop)

    for iter_i in range(n_iter):
        iter_dir = join(directory, "iter_{0}".format(iter_i))
        with open(iter_dir + '/execution_info.json', 'r') as fp:
            exp_info = json.load(fp)

        repair_list = exp_info["repaired_list"]
        for snapshot_i in range(n_snapshots):
            repair_matrix[iter_i, snapshot_i, :] = np.array(repair_list[snapshot_i])
    return repair_matrix


def load_members_values(directory: str, n_nodes: List[int]) -> List[np.array]:
    with open(directory + '/experiment_info.json', 'r') as fp:
        exp_info = json.load(fp)

    n_iter = exp_info["iter_count"]
    n_snapshots = exp_info["n_snapshots"]

    members_ts = [np.zeros(n_iter*node_size).reshape(n_iter, node_size) for node_size in n_nodes]
    for iter_i in range(n_iter):
        iter_dir = join(directory, "iter_{0}".format(iter_i))
        with open(iter_dir + '/execution_info.json', 'r') as fp:
            exp_info = json.load(fp)

        members_iter = exp_info["snapshot_members"]
        for snapshot_i in range(n_snapshots):
            members_ts[snapshot_i][iter_i, :] = np.array(members_iter[snapshot_i])

    return members_ts
