from __future__ import annotations

from functools import cached_property


class PlexVFSEpisode:
    def __init__(self, item):
        self.item = item

    def __str__(self):
        return self.title

    @cached_property
    def title(self):
        # Handle directory separator in filename
        title = self.item.title.replace("/", "∕")
        year = self.item.__dict__.get("year", None)
        if year:
            title += f" ({year})"

        guids = self.item.guids if self.item.guid.startswith("plex://") else []
        for guid in guids:
            title += f" {{{guid.id.replace('://', '-')}}}"

        return title
