import time
from functools import wraps


def timeit(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        start = time.time()
        res = func(*args, **kwargs)
        end = time.time()
        print("Elapsed Time: {:.4f}s".format(end - start))
        return res

    return wrapper
