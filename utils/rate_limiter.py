import time
import threading


class SimpleRateLimiter:
    def __init__(self, rate, cap=None, init_token=None):
        self._rate = rate
        self._prev_time = time.perf_counter()
        self._cap = cap if cap is not None else self._rate*2
        self._cap = max(self._cap, 1+1e-5)
        self._l = threading.Lock()
        self.token = min(init_token, self._cap) if init_token is not None else 0

    def ok(self, n=1):
        with self._l:
            cur = time.perf_counter()
            acc = (cur-self._prev_time)*self._rate
            self.token += acc
            self.token = min(self.token, self._cap)
            self._prev_time = cur
            if self.token >= n:
                self.token -= n
                return True
            return False

    def aquire(self, n=1, timeout=None):
        start = time.perf_counter()

        while True:
            if self.ok(n):
                return True
            if timeout is not None and time.perf_counter()-start >= timeout:
                return False
            time.sleep(0.01)
