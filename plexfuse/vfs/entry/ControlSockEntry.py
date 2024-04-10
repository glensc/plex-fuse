from __future__ import annotations

import stat

from plexfuse.vfs.entry.AttrEntry import AttrEntry


class ControlSockEntry(AttrEntry):
    def __init__(self, name: str, control_path: str):
        self.name = name
        self.size = 0
        self.link = control_path

    @property
    def attr(self):
        return {
            "st_mode": stat.S_IFLNK | 0o644
        }
