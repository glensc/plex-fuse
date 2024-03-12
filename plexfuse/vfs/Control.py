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
from plexfuse.vfs.entry.DirEntry import DirEntry

if TYPE_CHECKING:
    from plexfuse.fs.PlexFS import PlexFS
    from plexfuse.plex.PlexApi import PlexApi
    from plexfuse.vfs.PlexVFS import PlexVFS


class Control:
    def __init__(self, plex: PlexApi, plexfs: PlexFS, plexvfs: PlexVFS):
        self.plex = plex
        self.plexfs = plexfs
        self.plexvfs = plexvfs

    @property
    def root(self):
        return ["control"]

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

    def handle(self, pc: int, pe: list[str]):
        if pc == 1 and pe[0] in self.root:
            return DirEntry(self.commands)

        if pc != 2 or pe[0] != self.root[0]:
            return

        if pe[1] in self.commands:
            return ControlEntry(pe[1], getattr(self, pe[1]))
