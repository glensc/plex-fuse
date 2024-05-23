from __future__ import annotations

from collections import defaultdict
from functools import cached_property
from typing import TYPE_CHECKING

from plexfuse.normalize import normalize
from plexfuse.vfs.entry.SectionEntry import SectionEntry

if TYPE_CHECKING:
    from plexapi.library import Library


class LibraryEntry:
    def __init__(self, library: Library):
        self.library = library

    @cached_property
    def sections(self):
        return [SectionEntry(s) for s in self.library.sections()]

    @property
    def section_types(self):
        return self.sections_by_type.keys()

    @cached_property
    def sections_by_type(self):
        d = defaultdict(list)
        for s in self.sections:
            # Not yet there
            if s.type == "artist":
                continue
            d[s.type].append(s)
        return d

    @cached_property
    def section_by_title(self):
        return dict({(normalize(s.title), s) for s in self.sections})
