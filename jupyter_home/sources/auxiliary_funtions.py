import random
from operator import attrgetter

import igraph


def decode(chrom):
    """
    Returns the communities of a locus-based adjacency codification
    in a vector of int where each position is a node id and the value
    of that position the id of the community where it belongs. To position
    with the same number means that those two nodes belongs to same community.
    """
    try:
        size = len(chrom)
        last_c = 0
        communities = [float("inf")] * size
        pending = set(range(size))

        while len(pending) != 0:
            index = pending.pop()
            neighbour = chrom[index]

            if neighbour != -1:
                communities[index] = min(last_c, communities[index], communities[neighbour])
                while neighbour in pending:
                    pending.remove(neighbour)
                    communities[neighbour] = min(last_c, communities[neighbour])
                    neighbour = chrom[neighbour]
            last_c += 1
        return communities
    except Exception as e:
        raise e


def evaluate_individual(individual, graph: igraph.Graph):
    """
    Decode an individual into a community membership vector and
    calculates the modularity of the individual community set.
    """
    members = decode(individual)
    try:
        return max(0, graph.modularity(members)),
    except igraph.InternalError as e:
        raise RuntimeError("individual: {0}, members:{1}. raise the exception {2}".format(individual, members, e))


def flip_coin_with_probability(probability: float):
    """
    Returns 0 or 1 with the given probability
    """
    value = 0
    if random.random() <= probability:
        value = 1
    return value


def mutate_individual(individual, graph: igraph.Graph, probability: float):
    """
    Mutate each gen of the individual with the given probability to a random
    neighbor of the node with same id as the gen position
    """
    size = len(individual)

    for i in range(size):
        if flip_coin_with_probability(probability) is 1:
            neighbors = graph.neighborhood(vertices=i)
            individual[i] = neighbors[random.randint(0, len(neighbors) - 1)]

    return individual,


def create_individual(container, graph: igraph.Graph, n: int):
    """
    Creates a random individual creating each gen by selecting a random neighbor of
    the node with same id as the gen position
    """
    ind = container([None] * n)

    for i in range(n):
        neighbors = graph.neighborhood(vertices=i)
        ind[i] = neighbors[random.randint(0, len(neighbors) - 1)]

    return ind


def make_members_with_name(individual, graph):
    members = decode(individual)
    members_name = {}

    for i in range(len(members)):
        name = graph.vs[i]["name"]
        members_name[name] = members[i]

    return members_name


def random_neighbor(graph, vertex_index):
    neighbors = graph.neighborhood(vertices=vertex_index)
    return neighbors[random.randint(0, len(neighbors) - 1)]


def do_random_walk(num_steps, members: dict, graph: igraph.Graph, v_index: int):
    steps_done = 0
    communities = {
        -1: 0
    }

    actual_index = v_index
    while steps_done <= num_steps:
        actual_index = random_neighbor(graph, actual_index)
        actual_name = graph.vs[actual_index]["name"]
        if actual_name in members:
            com_id = members[actual_name]
        else:
            com_id = -1

        if com_id not in communities:
            communities[com_id] = 0
        communities[com_id] += 1

        steps_done += 1
    return communities
