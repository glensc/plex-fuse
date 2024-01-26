from collections import UserDict, defaultdict


class RefCountedDict(UserDict):
    def __init__(self):
        super().__init__()
        self.refcount = defaultdict(int)

    def __setitem__(self, key, value):
        self.refcount[key] += 1
        super().__setitem__(key, value)

    def __delitem__(self, key):
        self.refcount[key] -= 1
        if self.refcount[key] <= 0:
            super().__delitem__(key)
