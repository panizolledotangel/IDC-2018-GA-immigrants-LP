from random import randint
from typing import List, Dict

import igraph
import numpy as np
import matplotlib.pyplot as plt

import sources.experiment.metrics as metrics


def best_vs_best_median_one_graph(img_path, matrix_list, matrix_labels, num_snapshots, title):
    font = {'family': 'DejaVu Sans',
            'weight': 'bold',
            'size': 16}

    num_matrix = len(matrix_list)

    for snapshot_i in range(num_snapshots):
        f, axs = plt.subplots(1)
        f.set_size_inches(w=10, h=10)

        actual_ax = axs
        for i in range(num_matrix):
            immigrant = matrix_list[i]

            y_values = metrics.median_best(immigrant, snapshot_i)
            y_max_values = metrics.max_best(immigrant, snapshot_i)
            y_min_values = metrics.min_best(immigrant, snapshot_i)

            x_values = range(y_values.shape[0])
            actual_ax.plot(x_values, y_values, label=matrix_labels[i], linewidth=3.0)
            actual_ax.fill_between(x_values, y_min_values, y_max_values, alpha=0.5)

        actual_ax.set_title("snapshot {0} - {1}".format(snapshot_i, title), fontdict=font)
        axs.set_xlabel("generation number", fontdict=font)
        axs.set_ylabel("fitness value", fontdict=font)
        actual_ax.grid(color='gray', linestyle='-', linewidth=0.5)

        plt.savefig("{0}_snapshot{1}".format(img_path,snapshot_i))


def max_min_median_best_generation(img_path, matrix_repair, matrix_standard, num_snapshots, title):
    f, axs = plt.subplots(num_snapshots, 2, sharey='row')
    f.set_size_inches(w=20, h=10*num_snapshots)

    for snapshot_i in range(num_snapshots):
        actual_ax = axs[snapshot_i]

        y_values_med = metrics.median_best(matrix_repair, snapshot_i)
        x_values_med = range(y_values_med.shape[0])
        actual_ax[0].plot(x_values_med, y_values_med, label="median_greedy")

        y_values_max = metrics.max_best(matrix_repair, snapshot_i)
        x_values_max = range(y_values_max.shape[0])
        actual_ax[0].plot(x_values_max, y_values_max, label="best_greedy")

        y_values_min = metrics.min_best(matrix_repair, snapshot_i)
        x_values_min = range(y_values_min.shape[0])
        actual_ax[0].plot(x_values_min, y_values_min, label="worse_greedy")

        y_values_med = metrics.median_best(matrix_standard, snapshot_i)
        x_values_med = range(y_values_med.shape[0])
        actual_ax[1].plot(x_values_med, y_values_med, label="median_std")

        y_values_max = metrics.max_best(matrix_standard, snapshot_i)
        x_values_max = range(y_values_max.shape[0])
        actual_ax[1].plot(x_values_max, y_values_max, label="best_std")

        y_values_min = metrics.min_best(matrix_standard, snapshot_i)
        x_values_min = range(y_values_min.shape[0])
        actual_ax[1].plot(x_values_min, y_values_min, label="worse_std")

        actual_ax[0].set_title("TS {0} - {1}".format(snapshot_i, title))
        actual_ax[0].grid(color='gray', linestyle='-', linewidth=0.5)
        actual_ax[0].legend()

        actual_ax[1].set_title("TS {0} - {1}".format(snapshot_i, title))
        actual_ax[1].grid(color='gray', linestyle='-', linewidth=0.5)
        actual_ax[1].legend()

    plt.savefig(img_path)


def plot_first_individual_improvement(axs, immigrants_maxtrix_list, standard_matrix, matrix_labels, num_snapshots,
                                      title, ylabel, legend=True):
    width = 0.2
    num_matrix = len(immigrants_maxtrix_list)

    g_range = np.arange(num_snapshots) * ((num_matrix + 1) * width)
    g_spacing = np.arange(-num_matrix * width / 2, num_matrix * width / 2, width)

    standard = metrics.median_best_first(standard_matrix)
    for i in range(num_matrix):
        actual = metrics.median_best_first(immigrants_maxtrix_list[i])
        axs.bar(g_range + g_spacing[i], actual - standard, width, label=matrix_labels[i])

    labels = ["S({0})".format(i) for i in range(num_snapshots)]
    plt.setp(axs, xticks=g_range, xticklabels=labels)

    if legend:
        axs.legend()

    axs.grid(color='gray', linestyle='-', linewidth=0.5)
    axs.set_ylabel(ylabel)
    axs.set_title(title)

