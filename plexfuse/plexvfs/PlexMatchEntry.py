from __future__ import annotations

from functools import cached_property

from plexfuse.plexvfs.Playable import Playable
from plexfuse.plexvfs.PlexMatch import PlexMatch


class PlexMatchEntry:
    def __init__(self, playable: Playable):
        self.playable = playable

    def read(self, offset: int, size: int):
        return self.content[offset:offset + size].encode()

    @cached_property
    def content(self):
        plexmatch = PlexMatch()

        return plexmatch.content(self.playable)

    @cached_property
    def size(self):
        return len(self.content)

    def __len__(self):
        return self.size
