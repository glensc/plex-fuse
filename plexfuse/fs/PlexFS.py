import errno
from functools import cache
from pathlib import Path
from threading import Lock

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.fs.RefCountedDict import RefCountedDict
from plexfuse.normalize import normalize
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.vfs.entry.DirEntry import DirEntry
from plexfuse.vfs.PlexVFS import PlexVFS


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        plex = PlexApi()
        self.vfs = PlexVFS(plex, self)
        self.cache_path = None
        self.http_cache = None
        self.file_map = RefCountedDict()
        self.iolock = Lock()

    def fsinit(self):
        # "cache_path" property doesn't get always initialized from options:
        # https://github.com/libfuse/python-fuse/issues/61#issuecomment-1902472620
        cache_path = self.cache_path if self.cache_path else PlexApi.CACHE_PATH
        PlexApi.CACHE_PATH = Path(cache_path).absolute()
        PlexApi.HTTP_CACHE = self.http_cache

    @cache
    def getattr(self, path: str):
        path = normalize(path, is_path=True)
        try:
            item = self.vfs[path]
        except KeyError as e:
            print(f"ERROR: getattr: Unsupported path: {e}")
            return -errno.ENOENT

        if isinstance(item, DirEntry):
            return PlexDirectory(st_nlink=2 + len(item))

        return PlexFile(st_size=item.size, **item.attr)

    @cache
    def readdir(self, path: str, offset: int):
        return list(self._readdir(path))

    def _readdir(self, path: str):
        for r in [".", ".."]:
            yield fuse.Direntry(r)

        try:
            it = self.vfs[path]
        except KeyError as e:
            print(f"ERROR: readdir({path}): {e}")
            return

        for r in it:
            yield fuse.Direntry(r)

    def read(self, path, size, offset):
        with self.iolock:
            entry = self.file_map[path]

            return entry.read(offset, size)

    def release(self, path, flags):
        with self.iolock:
            try:
                del self.file_map[path]
            except KeyError as e:
                print(f"ERROR: release({path}): {e}")
                return -errno.EINVAL

            return 0

    def open(self, path, flags):
        with self.iolock:
            try:
                entry = self.vfs[path]
            except KeyError as e:
                print(f"ERROR: open({path}): {e}")
                return -errno.ENOENT

            if isinstance(entry, DirEntry):
                return -errno.EISDIR

            self.file_map[path] = entry

            return 0
