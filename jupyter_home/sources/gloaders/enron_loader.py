from datetime import date, datetime, timedelta

import pandas
import igraph

from sources.gloaders.loader_interface import LoaderInterface


class EnronLoader(LoaderInterface):

    @classmethod
    def _remove_isolated_nodes(cls, g: igraph.Graph) -> igraph.Graph:
        components = g.components(mode=igraph.WEAK)

        max_size = 0
        nodes = None
        for actual_component in components:
            size = len(actual_component)
            if size > max_size:
                max_size = size
                nodes = actual_component

        return g.subgraph(nodes)

    @classmethod
    def _make_graph(cls, table: pandas.DataFrame, init_d: datetime, end_d: datetime):
        t = table[(table['timestamp'] >= str(init_d)) & (table['timestamp'] <= str(end_d))]
        del t['timestamp']

        tuples = t.itertuples(index=False, name=None)
        graph = igraph.Graph.TupleList(tuples, weights=False)
        graph = EnronLoader._remove_isolated_nodes(graph)

        return graph

    @classmethod
    def _load_enron(cls, file_path: str, init_date: date, end_date: date, duration_snapshot: timedelta,
                    overlap: timedelta):

        t = pandas.read_csv(file_path)
        t = t[(t['timestamp'] >= str(init_date)) & (t['timestamp'] <= str(end_date))]

        t['week_day'] = t.apply(lambda row: datetime.strptime(row['timestamp'], "%Y-%m-%d %H:%M:%S").weekday(), axis=1)
        t = t[t['week_day'] < 5]
        del t['week_day']

        snapshots = []
        n_nodes = []
        n_edges = []

        # make date into datetime
        last_t = init_date + overlap

        while last_t < end_date:
            g_snapshot = EnronLoader._make_graph(t, last_t - overlap, last_t + duration_snapshot)
            snapshots.append(g_snapshot)
            n_nodes.append(g_snapshot.vcount())
            n_edges.append(g_snapshot.ecount())

            last_t += duration_snapshot

        return snapshots, n_nodes, n_edges

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

    def load_datatset(self, **kwargs) -> (list, int, list, list):
        snapshots, n_nodes, n_edges = EnronLoader._load_enron(kwargs["file"], kwargs["init_date"], kwargs["end_date"],
                                                              kwargs["duration_snapshot"], kwargs["overlap"])
        n_ts = len(snapshots)
        communities = None
        n_comms = None

        info = {
            "dataset_file": kwargs["file"],
            "init_date": str(kwargs["init_date"]),
            "end_date": str(kwargs["end_date"]),
            "duration_snapshot": str(kwargs["duration_snapshot"]),
            "snapshot_count": n_ts,
            "n_nodes": n_nodes,
            "n_edges": n_edges,
            "ground_truth": False,
            "memebers": communities,
            "n_communites": n_comms
        }
        return snapshots, n_ts, n_nodes, n_edges, info, communities, n_comms
