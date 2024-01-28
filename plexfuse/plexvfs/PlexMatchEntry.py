from __future__ import annotations


class PlexMatchEntry:
    def __init__(self, content: str):
        self.content = content
        self.size = len(content)

    def read(self, offset: int, size: int):
        return str.encode(self.content[offset:offset + size])

    def __len__(self):
        return self.size
