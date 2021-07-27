from functools import lru_cache

class Graph:
    def __init__(self, V: int):
        self._V = V
        self._E = None

    @property
    def V(self):
        return self._V

    @staticmethod
    def from_file(filename: str):
        pass

    @property
    def E(self):
        return self._E

    def add_edge(self, u, v) -> None:
        pass

    def get_adj(self, v):
        return

    @lru_cache()
    def get_degree(self, v):
        return len(self.get_adj(v))

