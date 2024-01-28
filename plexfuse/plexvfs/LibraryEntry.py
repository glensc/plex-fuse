from __future__ import annotations

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from plexapi.library import Library


class LibraryEntry:
    def __init__(self, library: Library):
        self.library = library
