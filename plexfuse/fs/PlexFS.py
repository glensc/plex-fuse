import errno

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.fs.PlexVFS import PlexVFS
from plexfuse.plex.PlexApi import PlexApi


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.plex = PlexApi()
        self.vfs = PlexVFS(self.plex)

    def getattr(self, path: str):
        try:
            item = self.vfs[path]
        except IndexError as e:
            print(e)
            return -errno.ENOENT

        pe = path.split("/")[1:]
        pc = len(pe)

        if pc == 4 and pe[0] == "movie":
            part = item[0]
            return PlexFile(st_size=part.size)

        return PlexDirectory(st_nlink=2 + len(item))

    def readdir(self, path: str, offset: int):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            it = self.vfs[path]
        except IndexError as e:
            print(e)
            return

        for r in it:
            yield fuse.Direntry(r)
