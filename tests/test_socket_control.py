from time import sleep

from plexfuse.control.ControlListener import ControlListener


def test_socket_control():
    s = ControlListener("/tmp/ControlListener.sock")
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
