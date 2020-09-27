import concurrent.futures as futures
import atexit

def at_new_thread(func):
    """
    return Future object
    """
    def wrapper(*args, **kwargs):
        executor = futures.ThreadPoolExecutor(1)
        fu = executor.submit(func, *args, **kwargs)
        atexit.register(executor.shutdown)
        return fu
    return wrapper