from __future__ import annotations

from functools import cached_property


class CachedPropertyCacheControl:
    """
    Cache control methods for an class using @cached_property
    """

    def __init__(self, obj):
        self.data = obj.__dict__
        self.name = obj.__class__.__name__
        self.members = self.find_members(obj.__class__)

    @staticmethod
    def find_members(cls):
        return [m for m in dir(cls) if isinstance(getattr(cls, m), cached_property)]

    def cache_info(self):
        yield f"{self.name} cache:"
        for k in self.members:
            v = self.data.get(k, None)
            f = f"{len(v)} items" if isinstance(v, (list, dict)) else v
            yield f"- {k}: {f}"

    def cache_clear(self):
        for k in self.members:
            try:
                del self.data[k]
                yield f"Deleted {self.name}: {k}"
            except KeyError:
                pass
