from functools import cached_property

from plexapi.server import PlexServer


class PlexApi:
    @cached_property
    def server(self):
        return PlexServer()

    @property
    def library(self):
        return self.server.library

    @cached_property
    def sections(self):
        return self.library.sections()

    @property
    def section_types(self):
        return {s.type for s in self.sections}

    def sections_by_type(self, type: str):
        return {s.title for s in self.sections if s.type == type}
