#!/bin/sh
#
# Installation:
# $ install -p contrib/plexfuse.sh ~/.local/bin/plexfuse
#
# Usage:
# $ plexfuse default
#
# This will help setup common variables and mount options.

# You can add per server configuration under case "$host" into ~/.config/plexfuse/init.sh:
#	case "$host" in
#	"default")
#		export PLEXAPI_AUTH_SERVER_BASEURL=http://localhost:32400
#		export PLEXAPI_AUTH_SERVER_TOKEN=xxx
#		;;
#	esac

die() {
	echo >&2 "ERROR: plexfuse: $*"
	exit 1
}

type mountpoint >/dev/null || mountpoint() {
	local path="$1"
	# Wrapper for systems missing "mountpoint", i.e. macOS
	# https://stackoverflow.com/questions/22192842/how-to-check-if-filepath-is-mounted-in-os-x-using-bash/22193352#22193352
	if mount | grep -q "on $path"; then
		return 0
	fi

	# try resolving symlink, i.e. "/tmp" may be symlink
	path=$(readlink -f "$path")
	[ -z "$path" ] && return 1

	if mount | grep -q "on $path"; then
		return 0
	fi

	return 1
}

main() {
	local host="${1:-}"; shift
	test -n "$host" || die "Need at least host argument"

	export XDG_CACHE_HOME=${XDG_CACHE_HOME:-$HOME/.cache}
	export XDG_CONFIG_HOME=${XDG_CONFIG_HOME:-$HOME/.config}
	export XDG_RUNTIME_DIR=${XDG_RUNTIME_DIR:-/run/user/$(id -u)}

	local cache_path="$XDG_CACHE_HOME/plexfuse/$host"
	local mount_path="$XDG_RUNTIME_DIR/plexfuse/$host"
	local config_path="$XDG_CONFIG_HOME/plexfuse/init.sh"
	local control_path="$cache_path/control.sock"
	local uid="${UID:-$(id -u)}"
	local gid="${GID:-$(id -g)}"
	local options="allow_other,ro,uid=$uid,gid=$gid,http_cache,cache_path=$cache_path,control_path=$control_path"

	# Add initialization, perhaps change values based on "$host"
	if [ -f "$config_path" ]; then
		. "$config_path"
	fi

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
