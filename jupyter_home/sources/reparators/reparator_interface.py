from abc import ABCMeta, abstractmethod
import igraph


class ReparatorInterface:
    _metaclass__ = ABCMeta

    def __init__(self, name: str):
        self.actual_snapshot = -1
        self.name = name

    def set_snapshot(self, snapshot_number: int):
        self.actual_snapshot = snapshot_number

    def get_name(self):
        return self.name

    @abstractmethod
    def repair(self, individual): raise NotImplementedError
