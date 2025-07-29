import time
from functools import wraps
import pandas as pd

CACHE = {}
TTL = 3600


def cache_df_with_custom_key(cache_key: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache_key in CACHE and CACHE[cache_key].get("expiry") - time.time() < TTL:
                return CACHE[cache_key]["data"]

            result: pd.DataFrame = func(*args, **kwargs)
            if result is not None and not result.empty:
                d = {"expiry": time.time(), "data": result}
                CACHE[cache_key] = d
                return result

            CACHE[cache_key]["expiry"] += TTL
            return CACHE[cache_key]["data"]

        return wrapper

    return decorator


def cache_dict_with_custom_key(cache_key: str):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            if cache_key in CACHE and time.time() - CACHE[cache_key].get("expiry") < TTL:
                return CACHE[cache_key]["data"]

            result: dict = func(*args, **kwargs)
            if result:
                d = {"expiry": time.time(), "data": result}
                CACHE[cache_key] = d
                return result

            CACHE[cache_key]["expiry"] += TTL
            return CACHE[cache_key]["data"]

        return wrapper

    return decorator


if __name__ == '__main__':
    a = time.time()
    time.sleep(5)
    print(time.time() - a)
