from __future__ import annotations


class DelayedPropertyCacheControl:
    """
    Cache control methods for class methods, but delayed
    """

    def __init__(self, obj, property: str, factory):
        self.obj = obj
        self.property = property
        self.factory = factory
        self.data = obj.__dict__

    def find_objects(self):
        return (self.factory(s) for s in self.data.get(self.property, []))

    def cache_info(self):
        for c in self.find_objects():
            yield from c.cache_info()

    def cache_clear(self):
        for c in self.find_objects():
            yield from c.cache_clear()
