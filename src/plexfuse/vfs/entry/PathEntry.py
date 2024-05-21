from __future__ import annotations

from pathlib import Path

from plexfuse.vfs.entry.AttrEntry import AttrEntry


class PathEntry(AttrEntry):
    def __init__(self, path: Path):
        self.path = path
        self.size = path.stat().st_size

    def read(self, offset: int, size: int):
        with self.path.open("rb") as fp:
            fp.seek(offset)
            return fp.read(size)

    def __len__(self):
        return self.size
