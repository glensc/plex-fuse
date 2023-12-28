# Plex FUSE Filesystem

An attempt to create fuse filesystem to access Plex Media Server.

## Development

This project is in very early development.

Currently implemented:
- [x] listing of root directory
- [x] Connecting to PMS via python-plexapi
- [x] Listing of library types in root directory
- [x] Listing library titles in library type sub-directory

## Plex Config

Create Plex [configuration] file:

```ini
# ~/.config/plexapi/config.ini

[auth]
server_baseurl = http://127.0.0.1:32400
server_token = XBHSMSJSDJ763JSm
```

[configuration]: https://python-plexapi.readthedocs.io/en/latest/configuration.html
