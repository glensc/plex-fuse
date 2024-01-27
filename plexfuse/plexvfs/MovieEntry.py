class MovieEntry:
    def __init__(self, item, title: str):
        self.item = item
        self.title = title

    def __str__(self):
        return self.title
