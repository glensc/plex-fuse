from contextlib import AbstractContextManager
from threading import Lock


class TimeoutLock(AbstractContextManager):
    def __init__(self, timeout: float = -1):
        self.lock = Lock()
        self.timeout = timeout
        self.result = None

    def __enter__(self):
        self.result = self.lock.acquire(timeout=self.timeout)
        if not self.result:
            raise RuntimeError(f"Unable to acquire lock in {self.timeout} seconds")
        return self

    def __exit__(self, __exc_type, __exc_value, __traceback):
        if self.result:
            self.lock.release()
        self.result = None
