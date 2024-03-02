from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from collections import UserDict


class UserDictCacheControl:
    """
    Cache control methods for an UserDict
    """

    def __init__(self, obj: UserDict):
        self.data = obj.data
        self.name = obj.__class__.__name__

    def cache_info(self):
        yield f"{self.name} cache:"
        for k, v in self.data.items():
            yield f"- {k}: {v.__class__.__name__}"

    def cache_clear(self):
        size = len(self.data)
        self.data.clear()
        yield f"Cleared {self.name} cache: {size} entries"
