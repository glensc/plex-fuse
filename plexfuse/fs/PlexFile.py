import stat
from time import time

from fuse import Stat


class PlexFile(Stat):
    def __init__(self, **kw):
        super().__init__(**kw)
        self.st_mode = stat.S_IFREG | 0o644
        self.st_nlink = 1
        self.st_atime = int(time())
        self.st_mtime = self.st_atime
        self.st_ctime = self.st_atime
