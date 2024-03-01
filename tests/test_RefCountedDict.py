from plexfuse.fs.RefCountedDict import RefCountedDict


def test_file():
    d = RefCountedDict()

    d["key1"] = "value1"
    assert "key1" in d, "set value and it's there"
    assert d["key1"] == "value1"

    d["key1"] = "value1"
    assert "key1" in d, "set value again with same value increases refcount"
    assert d["key1"] == "value1"

    try:
        d["key1"] = "value2"
        assert False, "setting different value must throw KeyError"
    except ValueError as e:
        assert str(e) == 'Value value2 already exists for key1', "Unexpected ValueError"

    del d["key1"]
    assert "key1" in d, "deleting will keep last value if refcount>0"
    assert d["key1"] == "value1"

    del d["key1"]
    assert "key1" not in d, "deleting last reference deletes key"
