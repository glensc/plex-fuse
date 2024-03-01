from __future__ import annotations

from functools import cached_property

from plexfuse.plexvfs.AttrEntry import AttrEntry


class ControlEntry(AttrEntry):
    def __init__(self, name: str, action):
        self.name = name
        self.action = action

    def read(self, offset: int, size: int):
        content = self.action()
        return content[offset:offset + size]

    @cached_property
    def size(self):
        return len(self.action())

    def __len__(self):
        return self.size
