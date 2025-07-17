#!/bin/sh
#
# Run container
#
# TODO:
#   cache_path=/wine/drive_c/users/root/AppData/Local/pip/cache
#	-v "$(pwd)/cache":$cache_path \
#
image=ghcr.io/tortugalabs/win-pyinstaller
exec docker run --rm -it \
	-v "$(pwd)":/src/ \
	"$image" \
	"$@"

