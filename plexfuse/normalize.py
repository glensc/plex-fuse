import unicodedata


def normalize(s: str, is_path=False):
    if not is_path:
        # Handle directory separator in filename
        s = s.replace("/", "∕")
    # Normalize Unicode
    # https://stackoverflow.com/questions/16467479/normalizing-unicode
    return unicodedata.normalize("NFC", s)
