from time import sleep

from plexfuse.control.Control import Control
from plexfuse.control.ControlListener import ControlListener
from plexfuse.fs.PlexFS import PlexFS
from plexfuse.plex.PlexApi import PlexApi
from plexfuse.vfs.PlexVFS import PlexVFS


def test_socket_control():
    p = PlexApi()
    fs = PlexFS()
    vfs = PlexVFS(p, fs)
    c = Control(p, fs, vfs)
    s = ControlListener("/tmp/ControlListener.sock", c)
    s.start()

    try:
        for i in range(100):
            print(f"Main thread idling: {i}...")
            sleep(10)
    except KeyboardInterrupt as e:
        print(e)
    finally:
        s.stop()
    print("Main thread exiting")


if __name__ == "__main__":
    test_socket_control()
