import errno
from functools import cache
from pathlib import Path
from threading import Lock

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.plex.ChunkedFile import ChunkedFile
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.PlexVFS import PlexVFS
from plexfuse.plex.PlexVFSFileEntry import PlexVFSFileEntry


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        plex = PlexApi()
        self.vfs = PlexVFS(plex)
        self.cache_path = None
        self.file_map = {}
        self.reader = ChunkedFile(plex)
        self.iolock = Lock()

    def fsinit(self):
        # "cache_path" property doesn't get always initialized from options:
        # https://github.com/libfuse/python-fuse/issues/61#issuecomment-1902472620
        cache_path = self.cache_path if self.cache_path else PlexApi.CACHE_PATH
        PlexApi.CACHE_PATH = Path(cache_path).absolute()

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
        file_path = self.file_map[path].key
        max_size = self.file_map[path].size

        with self.iolock:
            return self.reader.read(file_path, size=size, offset=offset, max_size=max_size)

    def release(self, path, flags):
        try:
            del self.file_map[path]
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

        self.file_map[path] = part

        return 0
