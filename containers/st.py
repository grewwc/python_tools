import bisect
from .convinient import ConvinientMixin
from typing import Dict


class BinarySearchEngine:
    """two arrays implementation
    """

    def __init__(self):
        self._keys = []
        self._values = []

    def get(self, key):
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            return self._values[idx]
        return None

    def put(self, key, value):
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            self._values[idx] = value
            return
        self._keys.insert(idx, key)
        self._values.insert(idx, value)

    def delete(self, key):
        idx = bisect.bisect_left(self._keys, key)
        if idx < len(self._keys) and self._keys[idx] == key:
            self._keys.pop(idx)
            self._values.pop(idx)

    def get_between(self, lo_key, hi_key=None):
        if len(self._keys) == 0:
            return {}

        if hi_key is None:
            hi_key = self._keys[-1]

        if lo_key >= hi_key:
            return {}
        lo_idx = bisect.bisect_left(self._keys, lo_key)
        if hi_key == len(self._keys):
            hi_idx = hi_idx
        else:
            hi_idx = bisect.bisect_right(self._keys, hi_key)
        return {k: v for k, v in zip(self._keys[lo_idx:hi_idx], self._values[lo_idx:hi_idx])}

    def __len__(self) -> int:
        return len(self._keys)

    def __contains__(self, key):
        return self.get(key) != None


class ST(ConvinientMixin):
    """all: get, put, delete, contains
    sorted: get_between
    """

    def __init__(self, engine=None):
        self._engine = engine if engine else BinarySearchEngine()

    def __repr__(self):
        return

    def get(self, key):
        return self._engine.get(key)

    def put(self, key, value):
        return self._engine.put(key, value)

    def delete(self, key):
        return self._engine.delete(key)

    def get_between(self, lo_key, hi_key=None) -> Dict:
        return self._engine.get_between(lo_key, hi_key)

    @staticmethod
    def from_dict(d: Dict):
        st = ST()
        for k, v in d:
            st.put(k, v)
        return st

    def to_dict(self) -> Dict:
        return {k: v for k, v in zip(self.keys, self.values)}

    @property
    def keys(self):
        return self._engine._keys

    @property
    def values(self):
        return self._engine._values

    def __len__(self):
        return self._engine.__len__()

    def __contains__(self, key):
        return self._engine.__contains__(key)
