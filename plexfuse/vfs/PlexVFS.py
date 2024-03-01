from __future__ import annotations

from collections import UserDict
from typing import TYPE_CHECKING

from plexfuse.vfs.ChunkedFile import ChunkedFile
from plexfuse.vfs.Control import Control
from plexfuse.vfs.entry.DirEntry import DirEntry
from plexfuse.vfs.entry.FileEntry import FileEntry
from plexfuse.vfs.entry.SubtitleEntry import SubtitleEntry
from plexfuse.vfs.entry.PlexMatchEntry import PlexMatchEntry

if TYPE_CHECKING:
    from plexfuse.fs.PlexFS import PlexFS
    from plexfuse.plex.PlexApi import PlexApi


class PlexVFS(UserDict):
    SUBTITLE_EXT = (".srt", ".vtt")

    def __init__(self, plex: PlexApi, plexfs: PlexFS):
        super().__init__()
        self.plex = plex
        self.reader = ChunkedFile(plex)
        self.control = Control(plex, plexfs, self)

    def __missing__(self, path: str):
        entry = self.resolve(path)
        if entry is None:
            raise KeyError(path)

        self[path] = entry

        return entry

    def resolve(self, path: str):
        if path == "/":
            ents = self.plex.section_types
            ents.extend(self.control.root)
            return DirEntry(ents)

        pe = path.split("/")[1:]
        pc = len(pe)

        try:
            resolved = self.control.handle(pc, pe)
            if resolved is not None:
                return resolved
        except KeyError:
            pass

        if pc == 1 and pe[0] in self["/"]:
            return DirEntry(list(self.plex.sections_by_type(pe[0])))
        elif pc == 2:
            entries = self.plex.library_items(pe[1])
            if entries is None:
                raise KeyError(pe)
            return DirEntry(entries)
        elif pc == 3 and pe[0] == "movie":
            mf = self.plex.movie_files(*pe[1:])
            if mf is None:
                raise KeyError(pe)
            return DirEntry(mf)
        elif pc == 3 and pe[0] == "show":
            seasons = self.plex.show_seasons(*pe[1:])
            if seasons is None:
                raise KeyError(pe)
            return DirEntry(seasons)
        elif pc == 4 and pe[0] in ["movie", "show"] and pe[3].endswith(".plexmatch"):
            playable = self.plex.library_item(*pe[1:-1])
            if playable is None:
                raise KeyError(pe)
            return PlexMatchEntry(playable)
        elif ((pc == 4 and pe[0] == "movie") or (pc == 6 and pe[0] == "show")) and pe[-1].endswith(self.SUBTITLE_EXT):
            if pe[0] == "movie":
                playable = self.plex.library_item(*pe[1:-1])
            elif pe[0] == "show":
                playable = self.plex.show_episode(*pe[1:-1])
            else:
                raise KeyError(pe)
            return SubtitleEntry(playable, name=pe[-1], plex=self.plex)
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
            packed = self.plex.episode_part(*pe[1:])
            if packed is None:
                raise KeyError(pe)
            part, playable = packed
            if part is None or playable is None:
                raise KeyError(pe)
            return FileEntry(part, playable=playable, reader=self.reader)
        elif pc == 4 and pe[0] == "movie":
            packed = self.plex.movie_part(*pe[1:])
            if packed is None:
                raise KeyError(pe)
            part, playable = packed
            if part is None or playable is None:
                raise KeyError(pe)
            return FileEntry(part, playable=playable, reader=self.reader)

        return None
