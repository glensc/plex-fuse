import unicodedata


def normalize(s: str):
    # Handle directory separator in filename
    s = s.replace("/", "∕")
    # Normalize Unicode
    # https://stackoverflow.com/questions/16467479/normalizing-unicode
    return unicodedata.normalize("NFC", s)
