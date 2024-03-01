from __future__ import annotations

from functools import cached_property

from plexfuse.vfs.entry.AttrEntry import AttrEntry


class ControlEntry(AttrEntry):
    def __init__(self, name: str, action):
        self.name = name
        self.action = action

    def read(self, offset: int, size: int):
        content = "\n".join(self.action()).encode() + b"\n"
        return content[offset:offset + size]

    @cached_property
    def size(self):
        # On macOS can't read from 0 byte file
        return 64 * 1024

    def __len__(self):
        return self.size
