from plexfuse.normalize import normalize


class DirEntry:
    def __init__(self, entries):
        self.entries = [normalize(str(s)) for s in entries]

    def __len__(self):
        return len(self.entries)

    def __iter__(self):
        return iter(self.entries)
