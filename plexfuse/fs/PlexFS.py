import errno
import os
from functools import cache

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.plex.DownloadCache import DownloadCache
from plexfuse.plex.FileCache import FileCache
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.PlexVFS import PlexVFS
from plexfuse.plex.PlexVFSFileEntry import PlexVFSFileEntry


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        plex = PlexApi()
        self.vfs = PlexVFS(plex)
        self.cache = DownloadCache(plex)
        self.cache_map = {}
        self.files = FileCache()

    @cache
    def getattr(self, path: str):
        try:
            item = self.vfs[path]
        except KeyError as e:
            print(f"getattr({path}): {e}")
            return -errno.ENOENT

        if isinstance(item, PlexVFSFileEntry):
            return PlexFile(st_size=item.size)

        return PlexDirectory(st_nlink=2 + len(item))

    @cache
    def readdir(self, path: str, offset: int):
        return list(self._readdir(path))

    def _readdir(self, path: str):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            it = self.vfs[path]
        except KeyError as e:
            print(f"readdir({path}): {e}")
            return

        for r in it:
            yield fuse.Direntry(str(r))

    def read(self, path, size, offset):
        try:
            cache_path = self.cache_map[path]
            with self.files[cache_path] as fh:
                fh.seek(offset, os.SEEK_SET)
                return fh.read(size)
        except KeyError:
            return -errno.EINVAL

    def release(self, path, flags):
        try:
            cache_path = self.cache_map[path]
            self.files.release(cache_path)
        except KeyError as e:
            print(f"release({path}): {e}")
            return -errno.EINVAL

        return 0

    def open(self, path, flags):
        try:
            part = self.vfs[path]
        except KeyError as e:
            print(f"open vfs({path}): {e}")
            return -errno.ENOENT

        if not isinstance(part, PlexVFSFileEntry):
            return -errno.EISDIR

        try:
            cache_path = self.cache[part]
        except KeyError as e:
            print(f"open cache({path}): {e}")
            self.cache[part] = None
            return -errno.ENOMEM

        if cache_path is None:
            return -errno.ENOMEM

        self.cache_map[path] = cache_path
        self.files.open(cache_path)

        return 0
