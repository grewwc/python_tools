from array import array
import math


class BloomFilter:

    def __init__(self) -> None:
        self._sz = 1024 * 1024
        self._arr = array('i', [0] * self._sz)

    def add(self, key):
        h = self._calc_h(key)
        while h > 0:
            idx = int(h % self._sz)
            self._arr[idx] += 1
            h = self._get_next_h(h)

    def remove(self, key) -> bool:
        h = self._calc_h(key)
        while h > 0:
            idx = idx(h % self._sz)
            if self._arr[idx] > 0:
                self._arr[idx] -= 1
            h = self._get_next_h(h)

    def exists(self, key) -> bool:
        h = self._calc_h(key)
        while h > 0:
            idx = int(h % self._sz)
            if self._arr[idx] <= 0:
                return False
            h = self._get_next_h(h)
        return True

    def __contains__(self, key) -> bool:
        return self.exists(key)

    def _calc_h(self, key):
        return abs(hash(key))

    def _get_next_h(self, h):
        return (h - 1) / 3
