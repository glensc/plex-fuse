from functools import cached_property

from plexapi.server import PlexServer


class PlexApi:
    @cached_property
    def server(self):
        return PlexServer()
