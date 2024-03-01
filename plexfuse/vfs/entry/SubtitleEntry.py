from __future__ import annotations

from functools import cached_property

from plexfuse.plex.PlexApi import PlexApi
from plexfuse.vfs.entry.AttrEntry import AttrEntry
from plexfuse.vfs.Playable import Playable


class SubtitleEntry(AttrEntry):
    def __init__(self, playable: Playable, name: str, plex: PlexApi):
        self.playable = playable
        self.name = name
        self.plex = plex

    def read(self, offset: int, size: int):
        with self.path.open("rb") as fp:
            fp.seek(offset)
            return fp.read(size)

    @property
    def attr(self):
        return self.playable.timestamps

    @cached_property
    def path(self):
        try:
            stream = self.playable.subtitles[self.name]
        except KeyError:
            return None

        cache_path = self.plex.cache_path(stream.key)
        if not cache_path.exists():
            print(f"Downloading: {cache_path}")
            self.plex.download_part(stream.key, cache_path)

        return cache_path

    @cached_property
    def size(self):
        return self.path.stat().st_size

    def __len__(self):
        return self.size
