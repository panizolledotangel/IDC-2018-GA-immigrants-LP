from typing import List
from sources.ga_config import GaConfiguration


class DynamicGaConfiguration:

    def __init__(self, ga_configs: List[GaConfiguration]):
        self.ga_configs = ga_configs
        self.actual_snapshot = -1

    def set_snapshot(self, n_snapshot: int):
        self.actual_snapshot = n_snapshot

    def get_ga_config(self):
        return self.ga_configs[self.actual_snapshot]

    def make_dict(self):
        d = {
            "n_snapshots": len(self.ga_configs),
            "ga_configs": [x.make_dict() for x in self.ga_configs]
        }
        return d
