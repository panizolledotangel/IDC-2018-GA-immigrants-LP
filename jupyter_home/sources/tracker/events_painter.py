import igraph
import numpy as np

from typing import List, Dict
from typing import Tuple

from sources.gloaders.loader_interface import LoaderInterface

STEP_COM = Tuple[List[str], int, str]
DY_COMMS = List[List[STEP_COM]]

EVENT_INFO = List[Dict[str, float]]


class EventsPainter:

    @classmethod
    def split_by_ts(cls, comm_events):
        events_by_ts = []
        accumulate = []
        last_ts = 0
        for event in comm_events:
            ts = event[1]
            if ts > last_ts:
                events_by_ts.append(accumulate)
                accumulate = []

            accumulate.append(event)
            last_ts = ts

        events_by_ts.append(accumulate)
        return events_by_ts

    @classmethod
    def _normalize_events_info(cls, events_info: EVENT_INFO):
        for i, events in enumerate(events_info):
            accumulate = 0
            for v in events.values():
                accumulate += v

            for event in events.keys():
                events_info[i][event] = events[event]/accumulate

    def __init__(self, dynamic_coms: DY_COMMS):
        self.dynamic_coms = dynamic_coms

    def important_nodes_events(self, loader: LoaderInterface) -> List[List[List[str]]]:
        n_ts = loader.get_dataset_info()["snapshot_count"]
        ts_coms = self._dcoms_by_ts(n_ts)

        important_nodes_events = [[] for _ in range(n_ts)]
        for ts in range(n_ts):
            snapshot = loader.snapshots[ts]
            centralities = np.array(snapshot.eigenvector_centrality())
            order_centrality_index = np.argsort(centralities)[::-1]

            top_names = [snapshot.vs[index]["name"] for index in order_centrality_index[0:10]]
            top_events = [[] for _ in range(len(top_names))]
            for top_i, name in enumerate(top_names):
                d_comms_ts = ts_coms[ts]
                for st_comm, event in d_comms_ts:
                    if name in st_comm:
                        top_events[top_i].append(event)
            important_nodes_events[ts] = top_events
        return important_nodes_events

    def get_events_info(self, n_ts: int) -> EVENT_INFO:
        events_ts_info = [{} for _ in range(n_ts)]
        for ts_d_comms in self.dynamic_coms:
            for step_com in ts_d_comms:
                static_com, ts, event = step_com

                if event not in events_ts_info[ts]:
                    events_ts_info[ts][event] = len(static_com)
                else:
                    events_ts_info[ts][event] += len(static_com)
        EventsPainter._normalize_events_info(events_ts_info)
        return events_ts_info

    def make_events_graph(self, filter_components=-1) -> igraph.Graph:
        g = igraph.Graph(directed=True)

        for i in range(len(self.dynamic_coms)):
            check = False
            if i != 0:
                check = True
            self._add_nodes(g, i, check)

        if filter_components > 0:
            index_destroy = []

            components = g.components(mode=igraph.WEAK)
            for cluster in components:
                if len(cluster) <= filter_components:
                    index_destroy.extend(cluster)

            g.delete_vertices(index_destroy)
        return g

    def paint_events(self, img_path: str, filter_components=-1):
        g = self.make_events_graph(filter_components)

        layers = [-1]*g.vcount()
        for i, v in enumerate(g.vs):
            layers[i] = v["ts"]

        visual_style = {"bbox": (10080, 900), "margin": 60, "vertex_size": 30, "vertex_label_size": 10,
                        "vertex_color": "green", "edge_width": 0.5,
                        "layout": g.layout_sugiyama(layers=layers, hgap=500), "vertex_label": g.vs["label"]}

        igraph.plot(g, img_path, **visual_style)

    def _add_nodes(self, g: igraph.Graph, com_id: int, check: bool):
        events_by_ts = EventsPainter.split_by_ts(self.dynamic_coms[com_id])

        prev_i = None
        for i in range(len(events_by_ts)):
            events = events_by_ts[i]
            added_names = []
            for event in events:
                ts = event[1]
                idcom = str(set(event[0]))
                idn = "{0}-{1}".format(ts, idcom)
                name = "C{0}.{1}".format(com_id, ts)
                added_names.append((idn, event[2]))

                if check:
                    found = g.vs.select(name=idn)
                    if len(found) == 0:
                        g.add_vertex(name=idn, label=name, ts=ts)
                else:
                    g.add_vertex(name=idn, label=name, ts=ts)

            if prev_i is not None:
                events = events_by_ts[prev_i]
                for event in events:
                    ts = event[1]
                    idcom = str(set(event[0]))
                    idn_s = "{0}-{1}".format(ts, idcom)

                    for idn_t, e_label in added_names:
                        g.add_edge(idn_s, idn_t, label=e_label)
            prev_i = i

    def _dcoms_by_ts(self, n_ts: int) -> List[List[Tuple[List[int], str]]]:
        events_ts_info = [[] for _ in range(n_ts)]
        for ts_d_comms in self.dynamic_coms:
            for step_com in ts_d_comms:
                static_com, ts, event = step_com
                events_ts_info[ts].append((static_com, event))
        return events_ts_info
