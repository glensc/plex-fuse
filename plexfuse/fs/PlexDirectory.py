import stat

from fuse import Stat


class PlexDirectory(Stat):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.st_mode = stat.S_IFDIR | 0o755
        self.st_nlink = 2
