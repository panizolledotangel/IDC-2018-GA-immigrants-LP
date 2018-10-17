from typing import List
from sources.ga_config import GaConfiguration
from sources.gas.dynamic_ga_configuration import DynamicGaConfiguration
from sources.reparators.reparator_interface import ReparatorInterface


class DynamicGaImmigrantsConfiguration(DynamicGaConfiguration):

    def __init__(self, ga_configs: List[GaConfiguration], rate_random_immigrants: List[float],
                 reparators: List[ReparatorInterface]):

        super().__init__(ga_configs)
        self.reparators = reparators
        self.rate_random_immigrants = rate_random_immigrants

    def get_reparator(self):
        return self.reparators[self.actual_snapshot]

    def get_rate_random_immigrants(self):
        return self.rate_random_immigrants[self.actual_snapshot]

    def make_dict(self):
        d = super().make_dict()
        d["reparators"] = [x.get_name() for x in self.reparators]
        d["rate_random_immigrants"] = self.rate_random_immigrants
        return d