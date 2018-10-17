import numpy as np


def max_best(matrix: np.array, num_snapshot: int) -> np.array:
    return np.max(matrix[:, num_snapshot, :, -1], axis=0)


def min_best(matrix: np.array, num_snapshot: int) -> np.array:
    return np.min(matrix[:, num_snapshot, :, -1], axis=0)


def median_best_first(matrix: np.array) -> np.array:
    return np.median(matrix[:, :, 0, -1], axis=0)


def median_best(matrix: np.array, num_snapshot: int) -> np.array:
    return np.median(matrix[:, num_snapshot, :, -1], axis=0)


def median_median(matrix: np.array, num_snapshot: int) -> np.array:
    return np.median(matrix[:, num_snapshot, :, :], axis=[2, 0])


def median_worse(matrix: np.array, num_snapshot: int) -> np.array:
    return np.median(matrix[:, num_snapshot, :, 0], axis=0)


def mean_best(matrix: np.array, num_snapshot: int) -> np.array:
    return np.mean(matrix[:, num_snapshot, :, -1], axis=0)


def mean_median(matrix: np.array, num_snapshot: int) -> np.array:
    return np.mean(matrix[:, num_snapshot, :, :], axis=[2, 0])


def mean_worse(matrix: np.array, num_snapshot: int) -> np.array:
    return np.mean(matrix[:, num_snapshot, :, 0], axis=0)


def median_generation_max_reach(matrix: np.array) -> np.array:
    return np.median(np.argmax(matrix[:, :, :, -1], axis=2), axis=0)


def median_generation_value_reach(matrix: np.array, truc_matrix) -> np.array:
    clip_m = np.minimum(np.median(matrix[:, :, :, -1], axis=0), truc_matrix)
    return np.argmax(clip_m, axis=1)
