# Plex FUSE Filesystem

An attempt to create fuse filesystem to access Plex Media Server files as local files.

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
- [x] Fix "/" in directory names
- [x] Download movie files to cache, serve read operations from cache
- [x] Add `-o cache_path` option
- [x] Test that Plex Media Server allows requesting file by range
- [x] Use chunked read for file cache
- [x] Listing of Show seasons
- [x] Listing of Season episodes
- [x] Listing of Episode files
- [x] Downloading episode files
- [x] Unicode normalize titles
- [x] Support .plexmatch for Movies
- [x] Support timestamps for Movies
- [x] Support .plexmatch for Show directories
- [x] Add movie timestamps to .plexmatch files
- [ ] Add timestamps to directories
- [x] Add subtitle files for Movies
- [x] Add subtitle files for Episodes
- [x] Cache PlexAPI requests using requests-cache (`-o http_cache`)
- [ ] Publish package to pypi
- [ ] Add docker volume driver
- [ ] Add cache management (max size?)
- [ ] Add cache purge option (special file?)
- [ ] Detect need to refresh cache (add event listener)
- [ ] Handling of "artist" library type
- [x] Add "status" and "reload" control channels

## Requirements

1. Python >= 3.11
1. fuse, macfuse, osxfuse or [fuse-t] depending on your OS

[fuse-t]: https://github.com/macos-fuse-t/fuse-t

## Installation

1. Install [pipx]
1. Install `plex-fuse`: `pipx install plex-fuse`

[pipx]: https://pipx.pypa.io/stable/installation

## Usage

1. Check [requirements](#requirements) and [installation](#installation)
1. Create [config.ini](#plex-config) for `python-plexapi`
1. Mount the configured PMS somewhere, i.e `plex-server`: `mkdir plex-server; plex-fuse plex-server -f`
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
