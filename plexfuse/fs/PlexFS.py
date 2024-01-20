import errno
from functools import cache

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.PlexVFS import PlexVFS
from plexfuse.plex.PlexVFSFileEntry import PlexVFSFileEntry


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.vfs = PlexVFS(PlexApi())

    @cache
    def getattr(self, path: str):
        try:
            item = self.vfs[path]
        except IndexError as e:
            print(e)
            return -errno.ENOENT

        if isinstance(item, PlexVFSFileEntry):
            return PlexFile(st_size=item.size)

        return PlexDirectory(st_nlink=2 + len(item))

    @cache
    def readdir(self, path: str, offset: int):
        return list(self._readdir(path, offset))

    def _readdir(self, path: str, offset: int):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            it = self.vfs[path]
        except IndexError as e:
            print(e)
            return

        for r in it:
            yield fuse.Direntry(str(r))
