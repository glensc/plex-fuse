from __future__ import annotations

import stat

from plexfuse.vfs.entry.AttrEntry import AttrEntry


class SymlinkEntry(AttrEntry):
    @property
    def size(self):
        return 0

    @property
    def link(self):
        raise NotImplementedError("Must implement link property")

    @property
    def attr(self):
        return {
            "st_mode": stat.S_IFLNK | 0o644
        }
