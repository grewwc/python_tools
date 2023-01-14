from threading import RLock, Condition


class CountDownLatch:
    def __init__(self, n):
        self._count = n
        self._cond = Condition(RLock())

    def count_down(self):
        with self._cond:
            self._count -= 1
            if self._count <= 0:
                self._cond.notify_all()

    def wait(self):
        with self._cond:
            while self._count > 0:
                self._cond.wait()
                
    def reset(self, n):
        with self._cond:
            if self._count > 0:
                raise RuntimeError("count > 0, can't reset! ")
            self._count = n
