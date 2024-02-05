import errno
from functools import cache
from pathlib import Path
from threading import Lock

import fuse

from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.normalize import normalize
from plexfuse.plex.ChunkedFile import ChunkedFile
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.plex.RefCountedDict import RefCountedDict
from plexfuse.plexvfs.DirEntry import DirEntry
from plexfuse.plexvfs.FileEntry import FileEntry
from plexfuse.plexvfs.PathEntry import PathEntry
from plexfuse.plexvfs.PlexMatchEntry import PlexMatchEntry
from plexfuse.plexvfs.PlexVFS import PlexVFS


class PlexFS(fuse.Fuse):
    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        plex = PlexApi()
        self.vfs = PlexVFS(plex)
        self.cache_path = None
        self.file_map = RefCountedDict()
        self.reader = ChunkedFile(plex)
        self.iolock = Lock()

    def fsinit(self):
        # "cache_path" property doesn't get always initialized from options:
        # https://github.com/libfuse/python-fuse/issues/61#issuecomment-1902472620
        cache_path = self.cache_path if self.cache_path else PlexApi.CACHE_PATH
        PlexApi.CACHE_PATH = Path(cache_path).absolute()

    @cache
    def getattr(self, path: str):
        path = normalize(path, is_path=True)
        try:
            item = self.vfs[path]
        except KeyError as e:
            print(f"ERROR: getattr: Unsupported path: {e}")
            return -errno.ENOENT

        if isinstance(item, (FileEntry, PlexMatchEntry, PathEntry)):
            kwargs = item.timestamps() if isinstance(item, FileEntry) else {}
            return PlexFile(st_size=item.size, **kwargs)

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
            yield fuse.Direntry(r)

    def read(self, path, size, offset):
        with self.iolock:
            entry = self.file_map[path]

            # Handle .plexmatch differently
            if isinstance(entry, PlexMatchEntry):
                return entry.read(offset, size)
            # Subtitles via PathEntry cache
            if isinstance(entry, PathEntry):
                return entry.read(offset, size)

            return self.reader.read(entry.key, size=size, offset=offset, max_size=entry.size)

    def release(self, path, flags):
        with self.iolock:
            try:
                del self.file_map[path]
            except KeyError as e:
                print(f"release({path}): {e}")
                return -errno.EINVAL

            return 0

    def open(self, path, flags):
        with self.iolock:
            try:
                part = self.vfs[path]
            except KeyError as e:
                print(f"open vfs({path}): {e}")
                return -errno.ENOENT

            if isinstance(part, DirEntry):
                return -errno.EISDIR

            self.file_map[path] = part

            return 0
