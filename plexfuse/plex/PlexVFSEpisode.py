from __future__ import annotations


class PlexVFSEpisode:
    def __init__(self, item):
        self.item = item
        self.title = item.title

    def __str__(self):
        return self.title
