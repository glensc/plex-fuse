from plexfuse.plex.RefCountedDict import RefCountedDict


def test_file():
    d = RefCountedDict()

    d["key1"] = "value1"
    assert "key1" in d, "set value and it's there"
    assert d["key1"] == "value1"

    d["key1"] = "value2"
    assert "key1" in d, "set value and it overwrites previous value"
    assert d["key1"] == "value2"

    del d["key1"]
    assert "key1" in d, "deleting will keep last value if refcount>0"
    assert d["key1"] == "value2"

    del d["key1"]
    assert "key1" not in d, "deleting last reference deletes key"
