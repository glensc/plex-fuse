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

    @cached_property
    def section_types(self):
        return {s.type for s in self.sections}
