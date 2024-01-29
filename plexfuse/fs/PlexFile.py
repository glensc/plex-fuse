import stat

from fuse import Stat

from plexfuse.fs.Timestampable import Timestampable


class PlexFile(Stat, Timestampable):
    def __init__(self, **kw):
        super().__init__(**kw)
        Timestampable.__init__(self)
        self.st_mode = stat.S_IFREG | 0o644
        self.st_nlink = 1
