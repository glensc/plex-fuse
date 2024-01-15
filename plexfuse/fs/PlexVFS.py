from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class PlexVFS(UserDict):
    def __init__(self, plex: PlexApi):
        super().__init__()
        self.plex = plex

    def __missing__(self, path: str):
        entry = self.resolve(path)
        if entry is None:
            raise ValueError(f"Unsupported path: {path}")

        self[path] = list(entry)

        return self[path]

    def resolve(self, path: str):
        if path == "/":
            return self.plex.section_types

        pe = path.split("/")[1:]
        pc = len(pe)

        if pc == 1 and pe[0] in self["/"]:
            return self.plex.sections_by_type(pe[0])
        elif pc == 2:
            return self.plex.library_items_titles(pe[1])
        elif pc == 3 and pe[0] == "movie":
            item = self.plex.library_item(pe[1], pe[2])
            return self.plex.media_part_names(item)
        elif pc == 4 and pe[0] == "movie" \
                and (m := self.plex.library_item(pe[1], pe[2])) \
                and pe[3] in self.plex.media_part_names(m) \
                and (part := self.plex.media_parts_by_name(m, pe[3])):
            return [part]

        return None
