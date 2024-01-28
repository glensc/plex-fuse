import stat

from fuse import Stat

from plexfuse.fs.Timestampable import Timestampable


class PlexDirectory(Stat, Timestampable):
    def __init__(self, **kw):
        super().__init__(**kw)
        Timestampable.__init__(self)
        self.st_mode = stat.S_IFDIR | 0o755
