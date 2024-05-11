import errno
from functools import wraps

import plexapi
import requests
import urllib3

from plexfuse.sentry import capture_exception


def plex_errno(f):
    # https://stackoverflow.com/questions/28965795/how-can-i-reuse-exception-handling-code-for-multiple-functions-in-python
    """
    handle exceptions from plex setting appropriate errno
    """

    @wraps(f)
    def decorated(*args, **kwargs):
        try:
            return f(*args, **kwargs)
        except (urllib3.exceptions.ReadTimeoutError,
                requests.exceptions.ConnectionError,
                requests.exceptions.ReadTimeout,
                TimeoutError) as e:
            print(f"ERROR: Plex: {f.__module__}.{f.__name__}({args[1:]}, {kwargs}): {type(e)}: {e}")
            capture_exception(e)
            return -errno.ETIMEDOUT
        except plexapi.exceptions.BadRequest as e:
            print(f"ERROR: Plex: {f.__module__}.{f.__name__}({args[1:]}, {kwargs}): {e}")
            capture_exception(e)
            return -errno.ENETUNREACH
        except KeyError as e:
            print(f"ERROR: Plex: {f.__module__}.{f.__name__}: Unsupported path: {e}")
            return -errno.ENOENT
        except Exception as e:
            print(f"ERROR: Plex: Unknown error {type(e)}: {e}")
            capture_exception(e)
            return -errno.ENOENT

    return decorated
