import time
from functools import wraps

def timer(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        start = time.time()
        result = func(self, *args, **kwargs)
        end = time.time()
        duration = end - start
        if hasattr(self, "_logger"):
            self._logger.info(f"Function '{func.__name__}' executed in {duration:.4f} seconds.")
        else:
            print(f"Function '{func.__name__}' executed in {duration:.4f} seconds.")
        return result
    return wrapper