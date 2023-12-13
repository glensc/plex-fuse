#
# A FUSE filesystem for mounting a Plex Media Server in Python
#
# Mount with:
# $ plexfuse <mountpoint>
# And un-mount with:
# $ fusermount -u <mountpoint>
#

import fuse

from plexfuse.fs.PlexFS import PlexFS

fuse.fuse_python_api = (0, 2)


def main():
    usage = "PlexFS: A filesystem for mounting a Plex Media Server media\n\n"
    server = PlexFS(version="%prog " + fuse.__version__,
                    usage=usage + fuse.Fuse.fusage, dash_s_do="setsingle")
    server.parse(errex=1)
    server.main()


if __name__ == "__main__":
    main()
