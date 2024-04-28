from time import sleep

from plexfuse.TimeoutLock import TimeoutLock


def test_timeout_lock():
    lock = TimeoutLock()
    with lock:
        assert True, "1s lock"

    lock = TimeoutLock(1)
    with lock:
        assert True, "1s lock"

    lock = TimeoutLock(0.5)
    with lock:
        assert True, "0.5s lock"

        try:
            with lock:
                assert False, "Never reached"
        except RuntimeError:
            assert True, "Nested lock failure"

        sleep(1)
        assert True, "Tested nested lock"
