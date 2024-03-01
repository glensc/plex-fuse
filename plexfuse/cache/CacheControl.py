class CacheControl:
    """
    Cache control methods for an object
    """

    def __init__(self, obj):
        self.name = obj.__class__.__name__
        self.methods = self.find_methods(obj)

    @staticmethod
    def find_methods(obj):
        methods = (getattr(obj, k) for k in dir(obj))
        return [m for m in methods if getattr(m, "cache_clear", None)]

    def cache_info(self):
        for m in self.methods:
            yield f"{self.name} cache: {m.__name__}: {m.cache_info()}"

    def cache_clear(self):
        for m in self.methods:
            size = m.cache_info().currsize
            m.cache_clear()
            yield f"{self.name} cache: {m.__name__}: cleared {size} entries"
