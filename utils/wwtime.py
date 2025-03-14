"""
Module File: wwtime.py
Description: This module provides functions of timing.

Author: Icingworld
Date: 2025-03-14
Version: 0.1.0
"""

import time
from functools import wraps
from wwlog import logger

def timeit(msg = None, unit = "ms"):
    """
    Timer Decorator

    :param msg: customized output message, default is function name
    :param unit: time unit (ms = millisecond，s = second，m = minute)
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            result = func(*args, **kwargs)
            elapsed = time.time() - start_time
            
            time_unit = {
                "ms": f"{elapsed * 1000:.2f} 毫秒",
                "s": f"{elapsed:.2f} 秒",
                "m": f"{elapsed / 60:.2f} 分钟"
            }[unit]
            
            display_msg = msg or f"函数 {func.__name__} 运行耗时"
            logger.info(f"{display_msg}: {time_unit}")
            return result
        return wrapper
    return decorator
