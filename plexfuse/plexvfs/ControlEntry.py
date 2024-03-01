from __future__ import annotations

from functools import cached_property

from plexfuse.plexvfs.AttrEntry import AttrEntry


class ControlEntry(AttrEntry):
    def __init__(self, name: str):
        self.name = name

    def read(self, offset: int, size: int):
        return b""

    @cached_property
    def size(self):
        return 0

    def __len__(self):
        return self.size
