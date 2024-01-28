from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING

from plexfuse.plexvfs.DirEntry import DirEntry
from plexfuse.plexvfs.FileEntry import FileEntry

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi


class PlexVFS(UserDict):
    def __init__(self, plex: PlexApi):
        super().__init__()
        self.plex = plex

    def __missing__(self, path: str):
        entry = self.resolve(path)
        if entry is None:
            raise KeyError(path)

        self[path] = entry

        return entry

    def resolve(self, path: str):
        if path == "/":
            return DirEntry(self.plex.section_types)

        pe = path.split("/")[1:]
        pc = len(pe)

        if pc == 1 and pe[0] in self["/"]:
            return DirEntry(list(self.plex.sections_by_type(pe[0])))
        elif pc == 2:
            return DirEntry(list(self.plex.library_items_titles(pe[1])))
        elif pc == 3 and pe[0] == "movie":
            movie = self.plex.library_item(*pe[1:])
            if movie is None:
                raise KeyError(pe)
            return DirEntry(list(self.plex.media_part_names(movie)))
        elif pc == 3 and pe[0] == "show":
            seasons = self.plex.show_seasons(*pe[1:])
            if seasons is None:
                raise KeyError(pe)
            return DirEntry(seasons)
        elif pc == 4 and pe[0] == "show":
            episodes = self.plex.season_episodes(*pe[1:])
            if episodes is None:
                raise KeyError(pe)
            return DirEntry(episodes)
        elif pc == 5 and pe[0] == "show":
            names = self.plex.episode_files(*pe[1:])
            if names is None:
                raise KeyError(pe)
            return DirEntry(names)
        elif pc == 6 and pe[0] == "show":
            part = self.plex.episode_part(*pe[1:])
            if part is None:
                raise KeyError(pe)
            return FileEntry(part)
        elif pc == 4 and pe[0] == "movie" \
                and (m := self.plex.library_item(pe[1], pe[2])) \
                and pe[3] in self.plex.media_part_names(m) \
                and (part := self.plex.media_parts_by_name(m, pe[3])):
            return FileEntry(part)

        return None