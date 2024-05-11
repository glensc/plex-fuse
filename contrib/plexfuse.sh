#!/bin/sh
#
# Installation:
# $ install -p contrib/plexfuse.sh ~/.local/bin/plexfuse
#
# Usage:
# $ plexfuse default
#
# This will help setup common variables and mount options
# You can add per server configuration under case "$host".

main() {
	local host="$1"; shift

	export XDG_CACHE_HOME=${XDG_CACHE_HOME:-$HOME/.cache}
	export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}

	local cache_path="$XDG_CACHE_HOME/plexfuse/$host"
	local mount_path="$XDG_RUNTIME_DIR/plexfuse/$host"
	local control_path="$cache_path/control.sock"
	local options="allow_other,ro,uid=1000,gid=1000,http_cache,cache_path=$cache_path,control_path=$control_path"

	case "$host" in
	"default")
		export PLEXAPI_AUTH_SERVER_BASEURL=http://localhost:32400
		export PLEXAPI_AUTH_SERVER_TOKEN=xxx
		;;
	*)
		exit >&2 "Unsupported host: $host"
		exit 2
		;;
	esac


	if mountpoint "$mount_path" -q; then
		umount "$mount_path"
	fi

	install -d "$mount_path" "$cache_path"

	export PYTHONUNBUFFERED=1
	exec plex-fuse -o "$options" "$mount_path" "$@"
}

set -eu
test -n "${TRACE:-}" && set -x
main "$@"
