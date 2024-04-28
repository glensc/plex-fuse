import errno
from functools import cache, cached_property
from pathlib import Path

import fuse

from plexfuse.control.Control import Control
from plexfuse.control.ControlListener import ControlListener
from plexfuse.fs.FsOptions import FsOptions
from plexfuse.fs.PlexDirectory import PlexDirectory
from plexfuse.fs.PlexFile import PlexFile
from plexfuse.fs.RefCountedDict import RefCountedDict
from plexfuse.normalize import normalize
from plexfuse.plex.Monitor import Monitor
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.TimeoutLock import TimeoutLock
from plexfuse.vfs.entry.DirEntry import DirEntry
from plexfuse.vfs.PlexVFS import PlexVFS


class PlexFS(fuse.Fuse):
    control: ControlListener | None
    monitor: Monitor | None

    def __init__(self, *args, **kw):
        super().__init__(*args, **kw)
        self.options = FsOptions()
        self.control = None
        self.monitor = None
        self.file_map = RefCountedDict()
        self.iolock = TimeoutLock(60)

    @cached_property
    def plex(self):
        return PlexApi()

    @cached_property
    def vfs(self):
        return PlexVFS(self.plex, self.options.control_path)

    def fsinit(self):
        # "cache_path" property doesn't get always initialized from options:
        # https://github.com/libfuse/python-fuse/issues/61#issuecomment-1902472620
        cache_path = self.options.cache_path if self.options.cache_path else PlexApi.CACHE_PATH
        PlexApi.CACHE_PATH = Path(cache_path).absolute()
        PlexApi.HTTP_CACHE = self.options.http_cache
        print(f"fsinit: CACHE_PATH={PlexApi.CACHE_PATH}")
        print(f"fsinit: HTTP_CACHE={PlexApi.HTTP_CACHE}")
        print(f"fsinit: control_path={self.options.control_path}")
        print(f"fsinit: listen_events={self.options.listen_events}")
        if self.options.control_path:
            control = Control(self.plex, self, self.vfs)
            self.control = ControlListener(self.options.control_path, control).start()
        if self.options.listen_events:
            self.monitor = Monitor(self.plex).start()

    def fsdestroy(self):
        if self.control:
            self.control.stop()

        if self.monitor:
            self.monitor.stop()

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
    def readlink(self, path: str):
        path = normalize(path, is_path=True)
        try:
            item = self.vfs[path]
        except KeyError as e:
            print(f"ERROR: readlink: Unsupported path: {e}")
            return -errno.ENOENT

        link = item.link
        if link is None:
            print(f"ERROR: readlink: value for {path} is None")
            return -errno.EINVAL

        return link

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
            print(f"Opened: {path}: {entry}")

            return 0
