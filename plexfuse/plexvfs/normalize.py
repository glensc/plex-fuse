import unicodedata


def normalize(s: str):
    # Normalize Unicode
    # https://stackoverflow.com/questions/16467479/normalizing-unicode
    return unicodedata.normalize("NFC", s)
