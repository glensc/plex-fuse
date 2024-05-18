from functools import wraps
from time import sleep

from plexapi.exceptions import BadRequest


def retry(retries: int, delay: int, fail: int):
    def decorator(fn):
        @wraps(fn)
        def wrapper(*args, **kwargs):
            count = 0
            while True:
                try:
                    return fn(*args, **kwargs)
                except (
                    BadRequest,
                ) as e:
                    if count == retries:
                        print(f"Error: {e}")
                        return fail

                    count += 1
                    name = f"{fn.__module__}.{fn.__name__}()"
                    print(
                        f"{e} for {name}, retrying after {delay} seconds (try: {count}/{retries})"
                    )
                    sleep(delay)

        return wrapper

    return decorator
