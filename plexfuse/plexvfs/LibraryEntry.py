from __future__ import annotations

from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.plexvfs.SectionEntry import SectionEntry

if TYPE_CHECKING:
    from plexapi.library import Library


class LibraryEntry:
    def __init__(self, library: Library):
        self.library = library

    @cached_property
    def sections(self):
        return [SectionEntry(s) for s in self.library.sections()]
