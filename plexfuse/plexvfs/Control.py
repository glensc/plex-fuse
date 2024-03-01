from __future__ import annotations

from typing import TYPE_CHECKING

from plexfuse.cache.CacheControl import CacheControl
from plexfuse.plexvfs.ControlEntry import ControlEntry
from plexfuse.plexvfs.DirEntry import DirEntry

if TYPE_CHECKING:
    from plexfuse.fs.PlexFS import PlexFS
    from plexfuse.plex.PlexApi import PlexApi


class Control:
    def __init__(self, plex: PlexApi, plexfs: PlexFS):
        self.plex = plex
        self.plexfs = CacheControl(plexfs)

    @property
    def root(self):
        return ["control"]

    @property
    def commands(self):
        return ["reload", "status"]

    def reload(self):
        yield from self.plexfs.cache_clear()

    def status(self):
        yield from self.plexfs.cache_info()

    def handle(self, pc: int, pe: list[str]):
        if pc == 1 and pe[0] in self.root:
            return DirEntry(self.commands)

        if pc != 2 or pe[0] != self.root[0]:
            return

        if pe[1] in self.commands:
            return ControlEntry(pe[1], getattr(self, pe[1]))
