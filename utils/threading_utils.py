from threading import RLock, Condition


class CountDownLatch:
    def __init__(self, n):
        self._count = n
        self._cond = Condition(RLock())

    def count_down(self):
        with self._cond:
            self._count -= 1
            if self._cond <= 0:
                self._cond.notify_all()

    def wait(self):
        with self._cond:
            while self._count > 0:
                self._cond.wait()
