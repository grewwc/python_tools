from threading import RLock, Condition, Lock, Thread
from concurrent.futures import ThreadPoolExecutor
from queue import Queue
import sys 
import os 
sys.path.append(os.path.dirname(__file__))
from rate_limiter import SimpleRateLimiter
import time 

_cost_name = "result.txt"

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


def multi_thread(func, n: int = 100, seconds: int = -1, max_workers: int = 10, rate_per_second: int=None, **kwargs):
    # clean cost file 
    with open(_cost_name, 'w') as f:
        pass
    p = ThreadPoolExecutor(max_workers=max_workers)
    q = Queue(maxsize=max_workers)
    l = Lock()
    result_list = []
    finished = False
    err_count = 0
    
    rate_limiter = SimpleRateLimiter(rate_per_second, 0)
    
    # 如果cost_list超过100，写入cost.txt
    def write(num_items):
        while True and not finished:
            l.acquire()
            if len(result_list) < num_items:
                l.release()
                time.sleep(1)
                continue
            else:
                with open(_cost_name, 'a+') as f:
                    f.write('\n'.join(result_list))
                    result_list.clear()
                    l.release()
                    f.write('\n')
                        
        with l:
            if finished and len(result_list) > 0:
                with open(_cost_name, 'a+') as f:
                    f.write('\n'.join(result_list))

    def poll(q):
        print('running')
        nonlocal finished, err_count
        while True:
            try:
                res = q.get()
                if res is None:
                    q.put(None)
                    finished = True
                    print("<<<< total time elapsed: {}".format(time.perf_counter() - start))
                    print('Error count: ', err_count)
                    return
                with l:
                    result_list.append(str(res[1].result()))
            except Exception as e:
                err_count += 1
            finally:
                if res is not None:
                    print("request #", res[0])

    Thread(target=poll, args=(q, )).start()
    Thread(target=write, args=(10, )).start()

    i = 1
    start = time.perf_counter()
    if seconds == -1:
        for i in range(n):
            rate_limiter.aquire()
            fu = p.submit(func, **kwargs)
            q.put((i, fu))
            i += 1
        q.put(None)

    else:
        end = seconds + start
        while time.perf_counter() < end:
            rate_limiter.aquire()
            fu = p.submit(func, **kwargs)
            q.put((i, fu))
            i += 1
        q.put(None)
    
    return result_list
