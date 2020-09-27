
from python_tools.wwcFunctions import minheapify, __swim, __sink

_swim, _sink = __swim, __sink # avoid class name mangling

class MinPQ:
    def __init__(self, data=None, key=lambda x: x):
        self._key = key 
        if data is not None:
            minheapify(data, key=self._key)
            self._data = list(data)
        else:
            self._data = []

    def put(self, item):
        self._data.append(item)
        _swim(self._data, len(self._data)-1, key=self._key)

    def get(self):
        res = self._data[0]
        self._data[0], self._data[-1] = self._data[-1], self._data[0]
        self._data.pop()
        _sink(self._data, 0, key=self._key)
        return res

    def peek(self):
        return self._data[0]

    def __len__(self):
        return len(self._data)

    def empty(self):
        return len(self) == 0

    @property
    def data(self):
        return self._data

class MaxPQ(MinPQ):
    def __init__(self, data=None, key=lambda x: x):
        self._key = lambda x: -key(x)
        super().__init__(data, self._key)
