import stat
from time import time

from fuse import Stat


class PlexDirectory(Stat):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.st_mode = stat.S_IFDIR | 0o755
        self.st_atime = int(time())
        self.st_mtime = self.st_atime
        self.st_ctime = self.st_atime
