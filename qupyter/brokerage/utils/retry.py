import asyncio
import time
from functools import wraps

def retry(exceptions, total_tries=5, delay=0.5, backoff=2, silently: bool = False):
    """
    Decorator for retrying function if exception occurs

    :param exceptions: exception(s) to check. can be a tuple of exceptions
    :param total_tries: total tries to attempt
    :param delay: initial delay between retry in seconds
    :param backoff: backoff multiplier e.g. value of 2 will double the delay each retry
    :return: Decorated function that will retry upon exceptions
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            current_try = 0
            while current_try < total_tries:
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    current_try += 1
                    sleep_time = delay * (backoff ** (current_try - 1))
                    if current_try != total_tries:
                        if not silently:
                            print(f"{str(e)}\nRetrying in {sleep_time} seconds...")
                        time.sleep(sleep_time)
                    else:
                        print("Max retry attempts reached, aborting.")
                        raise
        return wrapper
    return decorator

def async_retry(exceptions, total_tries=5, delay=0.5, backoff=2, silently: bool = False):
    """
    Decorator for retrying async function if exception occurs

    :param exceptions: exception(s) to check. can be a tuple of exceptions
    :param total_tries: total tries to attempt
    :param delay: initial delay between retry in seconds
    :param backoff: backoff multiplier e.g. value of 2 will double the delay each retry
    :return: Decorated async function that will retry upon exceptions
    """
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            current_try = 0
            while current_try < total_tries:
                try:
                    return await func(*args, **kwargs)
                except exceptions as e:
                    current_try += 1
                    sleep_time = delay * (backoff ** (current_try - 1))
                    if current_try != total_tries:
                        if not silently:
                            print(f"{str(e)}\nRetrying in {sleep_time} seconds...")
                        await asyncio.sleep(sleep_time)
                    else:
                        print("Max retry attempts reached, aborting.")
                        raise
        return wrapper
    return decorator