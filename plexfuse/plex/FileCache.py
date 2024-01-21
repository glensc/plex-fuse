from __future__ import annotations

from collections import UserDict, defaultdict
from contextlib import contextmanager
from pathlib import Path
from typing import BinaryIO


class FileCache(UserDict[str, BinaryIO]):
    def __init__(self):
        super().__init__()
        self.nopen = defaultdict(int)

    @contextmanager
    def cached_fh(self, path: str | Path):
        path = str(path)
        try:
            yield self.open(path)
        finally:
            self.release(path)

    def open(self, path: str):
        if path not in self:
            print(f"open: {path}, refcount={self.nopen[path]}")
            self[path] = self._open(path)
            self.nopen[path] += 1
            print(f"opened: {path}, refcount={self.nopen[path]}")

        return self[path]

    def release(self, path: str):
        if path not in self:
            raise KeyError

        self.nopen[path] -= 1
        if self.nopen[path] <= 0:
            print(f"close: {path}, refcount={self.nopen[path]}")
            fh = self[path]
            del self[path]
            fh.close()
            print(f"closed: {path}, refcount={self.nopen[path]}")

    def _open(self, path: str):
        try:
            fh = open(path, "rb")
        except Exception as e:
            raise Exception(e)
        return fh
