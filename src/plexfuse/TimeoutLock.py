from contextlib import AbstractContextManager
from threading import Lock


class TimeoutLock(AbstractContextManager):
    global_lock = Lock()

    def __init__(self, timeout: float = -1):
        self.lock = Lock()
        self.timeout = timeout
        self.result = None

    def acquire(self):
        self.global_lock.acquire()
        try:
            return self.lock.acquire(timeout=self.timeout)
        finally:
            self.global_lock.release()

    def release(self):
        self.global_lock.acquire()
        try:
            self.lock.release()
        finally:
            self.global_lock.release()

    def __enter__(self):
        self.result = self.acquire()
        if not self.result:
            raise RuntimeError(f"Unable to acquire lock in {self.timeout} seconds")
        return self

    def __exit__(self, __exc_type, __exc_value, __traceback):
        if self.result:
            self.release()
        self.result = None
