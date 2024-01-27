from __future__ import annotations

import os
from collections import UserDict
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexfuse.plex.PlexApi import PlexApi
    from plexfuse.plexvfs.FileEntry import FileEntry


class DownloadCache(UserDict):
    def __init__(self, plex: PlexApi):
        super().__init__()
        self.plex = plex

    def __getitem__(self, key):
        if key in self.data:
            # Invalidate cache if file has gone missing
            path = self.data[key]
            if not os.path.exists(path):
                del self[key]

        return super().__getitem__(key)

    def __missing__(self, part: FileEntry):
        path = self.resolve(part)
        if path is None:
            raise KeyError(f"Unsupported part: {part}")

        self[part] = path

        return path

    def resolve(self, part: FileEntry):
        savepath = self.plex.cache_path(part.key)
        return self.plex.download_part(part.key, savepath)
