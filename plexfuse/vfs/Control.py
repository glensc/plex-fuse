from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.cache.CacheControl import CacheControl
from plexfuse.cache.CachedPropertyCacheControl import \
    CachedPropertyCacheControl
from plexfuse.cache.DelayedPropertyCacheControl import \
    DelayedPropertyCacheControl
from plexfuse.cache.UserDictCacheControl import UserDictCacheControl
from plexfuse.vfs.entry.ControlEntry import ControlEntry
from plexfuse.vfs.entry.ControlSockEntry import ControlSockEntry
from plexfuse.vfs.entry.DirEntry import DirEntry

if TYPE_CHECKING:
    from plexfuse.fs.PlexFS import PlexFS
    from plexfuse.plex.PlexApi import PlexApi
    from plexfuse.vfs.PlexVFS import PlexVFS


class Control:
    CONTROL_DIR = "control"
    CONTROL_SOCK = "control.sock"

    def __init__(self, plex: PlexApi, plexfs: PlexFS, plexvfs: PlexVFS, control_path: str = None):
        self.plex = plex
        self.plexfs = plexfs
        self.plexvfs = plexvfs
        self.control_path = control_path

    @property
    def root(self):
        entries = [
            self.CONTROL_DIR,
        ]

        if self.control_path:
            entries.append(self.CONTROL_SOCK)

        return entries

    @property
    def commands(self):
        return ["reload", "status"]

    @cached_property
    def cc_plexfs(self):
        return CacheControl(self.plexfs)

    @cached_property
    def cc_plexvfs(self):
        return UserDictCacheControl(self.plexvfs)

    @cached_property
    def cc_library(self):
        return CachedPropertyCacheControl(self.plex.library)

    @cached_property
    def cc_sections(self):
        return DelayedPropertyCacheControl(self.plex.library, "sections", CachedPropertyCacheControl)

    def reload(self):
        yield from self.cc_plexfs.cache_clear()
        yield from self.cc_plexvfs.cache_clear()
        yield from self.cc_sections.cache_clear()
        yield from self.cc_library.cache_clear()

    def status(self):
        yield from self.cc_plexfs.cache_info()
        yield from self.cc_plexvfs.cache_info()
        yield from self.cc_sections.cache_info()
        yield from self.cc_library.cache_info()

    def action(self, action: str):
        method = getattr(self, action)
        return "\n".join(method()).encode() + b"\n"

    def handle(self, pc: int, pe: list[str]):
        if pc == 1 and pe[0] == self.CONTROL_SOCK:
            return ControlSockEntry(pe[0], self.control_path)

        if pc == 1 and pe[0] == self.CONTROL_DIR:
            return DirEntry(self.commands)

        if pc != 2 or pe[0] != self.CONTROL_DIR:
            return

        if pe[1] in self.commands:
            return ControlEntry(pe[1], getattr(self, pe[1]))
