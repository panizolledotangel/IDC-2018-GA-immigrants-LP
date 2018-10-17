from random import randint
from typing import List, Dict

import  igraph

from sources.gloaders.loader_interface import LoaderInterface


class CommunityGraphPainter:

    @classmethod
    def _find_commmunicating_community(cls, node_index: int, coms: Dict[int, List[int]]) -> int:
        found = -1
        i = 0
        keys = coms.keys()
        while found == -1 and i < len(keys):
            if node_index in coms[keys[i]]:
                found = keys[i]
            i += 1
        return found

    def __init__(self, dataset: LoaderInterface, members: List[List[int]]):
        self.dataset = dataset
        self.members = members

        n_nodes = self.dataset.get_dataset_info()["n_nodes"]
        self.available_colors = ['%06X' % randint(0, 0xFFFFFF) for _ in range(max(n_nodes))]

    def plot_results_communities_graph(self, out_dir: str, img_name: str):
        n_snapshots = self.dataset.get_dataset_info()["snapshot_count"]

        for ts in range(n_snapshots):
            g = igraph.Graph()

            meta_coms = self._order_in_communities(ts)
            self._add_metacommunities_vertex(g, meta_coms)
            self._connect_metacomunities(ts, g, meta_coms)

    def _order_in_communities(self, ts: int) -> Dict[int, List[int]]:
        coms = {}
        for n_id, com_id in enumerate(self.members[ts]):
            if n_id not in coms:
                coms[n_id] = []
            coms[n_id].append(com_id)
        return coms

    def _add_metacommunities_vertex(self, g: igraph.Graph, meta_coms: Dict[int, List[int]]):
        for meta_id, meta_name in enumerate(meta_coms.keys()):
            g.add_vertex(name=meta_name, color=self.available_colors[meta_id], size=len(meta_coms[meta_name]))

    def _connect_metacomunities(self, ts: int, g: igraph.Graph, meta_coms: Dict[int, List[int]]):
        for meta_id, meta_name in enumerate(meta_coms.keys()):
            snapshot = self.dataset.snapshots[ts]
            for node_index in meta_coms[meta_name]:
                edges = snapshot.es.select(_source=node_index)
                for e in edges:
                    com_id = self._find_commmunicating_community(e.target, meta_coms)
                    actual_edge = g.es.find(_between=((meta_id,), (com_id,)))

                    if len(actual_edge) > 0:
                        actual_edge[0]["weight"] += 1
                    else:
                        g.add_edge(meta_id, com_id, weight=1)
