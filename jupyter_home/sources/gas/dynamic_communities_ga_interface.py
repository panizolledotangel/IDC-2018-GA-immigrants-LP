from abc import ABCMeta, abstractmethod


class DynamicCommunitiesGAInterface:
    _metaclass__ = ABCMeta

    def __init__(self, snapshots: list, individual_sizes: list, statistics_dir: str):

        self.snapshots = snapshots
        self.individual_sizes = individual_sizes
        self.statistics_dir = statistics_dir

    @abstractmethod
    def find_communities(self): raise NotImplementedError

    @abstractmethod
    def make_dict(self): raise NotImplemented
