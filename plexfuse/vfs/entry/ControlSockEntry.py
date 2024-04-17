from __future__ import annotations

from plexfuse.vfs.entry.SymlinkEntry import SymlinkEntry


class ControlSockEntry(SymlinkEntry):
    def __init__(self, name: str, control_path: str):
        self.name = name
        self.control_path = control_path

    @property
    def link(self):
        return self.control_path
