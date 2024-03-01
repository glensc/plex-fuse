from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.media import Guid

    from plexfuse.vfs.Playable import Playable


class PlexMatch:
    """
    Handler for .plexmatch files
    - https://support.plex.tv/articles/plexmatch/
    """

    def content(self, playable: Playable):
        return "\n".join(self.mapping(playable.guids))

    @staticmethod
    def mapping(guids: list[Guid]):
        for guid in guids:
            provider, value = guid.id.split("://")
            yield f"{provider}id: {value}"

        # Add newline to end of the file
        yield ""
