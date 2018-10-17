from abc import ABCMeta, abstractmethod

from sources.gloaders.loader_interface import LoaderInterface


class TestSuitInterface:
    _metaclass__ = ABCMeta

    def __init__(self, test_bench: LoaderInterface, output_dir: str, experiment_name: str, num_iter: int, ts_min=0,
                 ts_max=-1):

        self.test_bench = test_bench
        self.output_dir = output_dir
        self.experiment_name = experiment_name
        self.num_iter = num_iter
        self.ts_min = ts_min
        self.ts_max = ts_max

    @abstractmethod
    def do_test_suit(self, **kwargs): raise NotImplementedError

    @abstractmethod
    def get_test_suit_loader(self, **kwargs): raise NotImplementedError
