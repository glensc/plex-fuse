from __future__ import annotations

from collections import UserDict, defaultdict
from contextlib import contextmanager
from typing import BinaryIO


class FileCache(UserDict[str, BinaryIO]):
    def __init__(self):
        super().__init__()
        self.nopen = defaultdict(int)

    @contextmanager
    def cached_fh(self, path: str):
        try:
            yield self.open(path)
        finally:
            self.release(path)

    def open(self, path: str):
        if path not in self:
            self[path] = self._open(path)
            self.nopen[path] += 1

        return self[path]

    def release(self, path: str):
        if path not in self:
            raise KeyError

        self.nopen[path] -= 1
        if self.nopen[path] <= 0:
            fh = self[path]
            fh.close()
            del self[path]

    def _open(self, path: str):
        try:
            fh = open(path, "rb")
        except Exception as e:
            raise Exception(e)
        return fh
