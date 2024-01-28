from __future__ import annotations


class PlexMatchEntry:
    def __init__(self, content: str):
        self.content = content
        self.size = len(content)

    def __len__(self):
        return self.size
