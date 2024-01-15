# Plex FUSE Filesystem

An attempt to create fuse filesystem to access Plex Media Server.

## Development

This project is in very early development.

Currently implemented:
- [x] Listing of root directory
- [x] Connecting to PMS via python-plexapi
- [x] Listing of library types in root directory
- [x] Listing library titles in library type sub-directory
- [x] Listing titles from a library
- [x] Listing of Movie files
- [x] Report file size for media part
- [x] Report accurate nlink for directories
- [x] Memoize readdir and getattr calls
- [ ] Listing of Show seasons
- [ ] Listing of Season episodes
- [ ] Listing of Episode files
- [ ] Handling of "artist" library type
- [ ] Fix "/" in directory names

## Usage

1. Install Python >= 3.10
1. Install fuse, macfuse, osxfuse, [fuse-t](https://github.com/macos-fuse-t/fuse-t) depending on your OS
1. Install [pipenv](https://pipenv.pypa.io/en/latest/installation.html)
1. Clone this project: `git clone https://github.com/glensc/plex-fuse`
1. Change to `plex-fuse` directory
1. Install project dependencies `pipenv install`
1. Create [config.ini](#plex-config) for `python-plex`
1. Mount the configured PMS somewhere, i.e `plex-server`: `mkdir plex-server; pipenv run python -m plexfuse plex-server -f`
1. Access the `plex-server` directory from another terminal
1. `umount` or `fusermount -u` the directory to remove the `plex-server` mount

## Plex Config

Create Plex [configuration] file:

```ini
# ~/.config/plexapi/config.ini

[auth]
server_baseurl = http://127.0.0.1:32400
server_token = XBHSMSJSDJ763JSm
```

[configuration]: https://python-plexapi.readthedocs.io/en/latest/configuration.html
