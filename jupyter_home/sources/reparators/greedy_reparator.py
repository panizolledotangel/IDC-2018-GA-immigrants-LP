import random
from typing import List

import igraph

from sources.auxiliary_funtions import make_members_with_name
from sources.reparators.reparator_interface import ReparatorInterface


class GreedyReparator(ReparatorInterface):

    @classmethod
    def _random_neighbor_most(cls, members, neighbors):
        def _add_member(n_members, comm_id, neig):
            if comm_id != float('inf'):
                if comm_id not in n_members:
                    n_members[comm_id] = []
                n_members[comm_id].append(neig)
                return len(n_members[comm_id])
            else:
                return -1

        neighbors_members = {}
        actual_len = 0
        actual_member = -1

        for nei in neighbors:
            if nei in members:
                com_id = members[nei]
                com_size = _add_member(neighbors_members, com_id, nei)

                if com_size > actual_len:
                    actual_len = com_size
                    actual_member = com_id

        if actual_member == -1:
            random_neig = neighbors[random.randint(0, len(neighbors) - 1)]
        else:
            m_neighbors = neighbors_members[actual_member]
            random_neig = m_neighbors[random.randint(0, len(m_neighbors) - 1)]

        return random_neig

    def __init__(self, name: str, snapshot_list: List[igraph.Graph], container):
        super().__init__(name)
        self.snapshot_list = snapshot_list
        self.container = container

    def repair(self, individual):
        old_g = self.snapshot_list[self.actual_snapshot - 1]
        new_g = self.snapshot_list[self.actual_snapshot]

        members_name = make_members_with_name(individual, old_g)

        old_g_size = old_g.vcount()
        new_g_size = new_g.vcount()
        min_size = min(old_g_size, new_g_size)

        new_individual = self.container([None]*new_g_size)
        pending = set(range(new_g_size))

        index = 0
        n_gen_repair = 0
        while len(pending) != 0 and index < min_size:
            s_name = old_g.vs[index]["name"]
            s_index = new_g.vs.select(name=s_name)

            t_name = old_g.vs[individual[index]]["name"]
            t_index = new_g.vs.select(name=t_name)

            if len(s_index) != 0:
                s_index = s_index[0].index
                neighbors = new_g.neighborhood(vertices=s_index)

                if len(t_index) != 0:
                    # both nodes exits
                    t_index = t_index[0].index

                    if t_index != s_index and t_index not in neighbors:
                        neig_names = [new_g.vs[x]["name"] for x in neighbors]
                        selected_name = GreedyReparator._random_neighbor_most(members_name, neig_names)
                        new_individual[s_index] = new_g.vs.select(name=selected_name)[0].index

                        n_gen_repair += 1
                    else:
                        new_individual[s_index] = t_index
                else:
                    # target don't exists
                    neig_names = [new_g.vs[x]["name"] for x in neighbors]
                    selected_name = GreedyReparator._random_neighbor_most(members_name, neig_names)
                    new_individual[s_index] = new_g.vs.select(name=selected_name)[0].index

                    n_gen_repair += 1
                pending.discard(s_index)
            index += 1

        while len(pending) != 0:
            n_gen_repair += 1
            index = pending.pop()

            neig_names = [new_g.vs[x]["name"] for x in new_g.neighborhood(vertices=index)]
            selected_name = GreedyReparator._random_neighbor_most(members_name, neig_names)
            new_individual[index] = new_g.vs.select(name=selected_name)[0].index

        return new_individual, n_gen_repair
