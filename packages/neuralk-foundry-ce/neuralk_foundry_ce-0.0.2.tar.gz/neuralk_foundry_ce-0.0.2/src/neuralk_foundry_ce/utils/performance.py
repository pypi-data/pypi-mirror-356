import time
from memory_profiler import memory_usage


def profile_function(func, *args, **kwargs):
    start_time = time.perf_counter()
    mem_usage, result = memory_usage((func, args, kwargs), retval=True)
    end_time = time.perf_counter()
    return result, mem_usage, end_time - start_time

