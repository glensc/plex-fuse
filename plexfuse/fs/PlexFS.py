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
        st = PlexDirectory()

        try:
            item = self.vfs[path]
        except ValueError as e:
            print(e)
            return -errno.ENOENT

        pe = path.split("/")[1:]
        pc = len(pe)

        if pc == 4 and pe[0] == "movie":
            part = item[0]
            return PlexFile(st_size=part.size)
        else:
            st.st_nlink = 2 + len(item)

        return st

    def readdir(self, path: str, offset: int):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            for r in self.vfs[path]:
                yield fuse.Direntry(r)
        except ValueError as e:
            print(e)
