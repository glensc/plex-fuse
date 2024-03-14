from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.vfs.entry.AttrEntry import AttrEntry

if TYPE_CHECKING:
    from plexapi.media import Guid

    from plexfuse.vfs.Playable import Playable


class PlexMatchEntry(AttrEntry):
    def __init__(self, playable: Playable):
        self.playable = playable

    def read(self, offset: int, size: int):
        return self.content[offset:offset + size].encode()

    @property
    def attr(self):
        return self.playable.timestamps

    @cached_property
    def content(self):
        """
        Handler for .plexmatch files
        - https://support.plex.tv/articles/plexmatch/
        """
        return "\n".join(self.mapping(self.playable.guids))

    @staticmethod
    def mapping(guids: list[Guid]):
        for guid in guids:
            provider, value = guid.id.split("://")
            yield f"{provider}id: {value}"

        # Add newline to end of the file
        yield ""

    @cached_property
    def size(self):
        return len(self.content)

    def __len__(self):
        return self.size
