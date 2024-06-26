#
# A FUSE filesystem for mounting a Plex Media Server in Python
#
# Mount with:
# $ plexfuse <mountpoint>
# And un-mount with:
# $ fusermount -u <mountpoint>
#

import fuse

from plexfuse.__version__ import __version__
from plexfuse.fs.PlexFS import PlexFS
from plexfuse.plex.PlexApi import PlexApi

fuse.fuse_python_api = (0, 2)


def main():
    usage = "PlexFS: A filesystem for mounting a Plex Media Server media\n\n"
    server = PlexFS(version=f"%prog: {__version__}\npython-fuse: {fuse.__version__}",
                    usage=usage + fuse.Fuse.fusage, dash_s_do="setsingle")
    server.parser.add_option(mountopt="cache_path", metavar="PATH",
                             default=PlexApi.CACHE_PATH,
                             help="cache downloads under PATH [default: %default]")
    server.parser.add_option(mountopt="http_cache",
                             default=False, action="store_true",
                             help="cache http requests using requests-cache")
    server.parser.add_option(mountopt="listen_events",
                             default=False, action="store_true",
                             help="listen for events from Plex Media Server")
    server.parser.add_option(mountopt="control_path", metavar="PATH",
                             default=None,
                             help="path to control socket [default: %default]")
    server.parser.add_option(mountopt="sentry_dsn", metavar="DSN",
                             default=None,
                             help="sentry dsn to enable logging to Sentry.io")
    server.parse(values=server.options, errex=1)
    server.main()


if __name__ == "__main__":
    main()
