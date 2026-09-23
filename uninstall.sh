#!/usr/bin/env bash
set -euo pipefail

APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/linkplayer"
BIN_DIR="${HOME}/.local/bin"
APP_MENU_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"
rm -f "$BIN_DIR/linkplayer" "$APP_MENU_DIR/linkplayer.desktop"
rm -rf "$APP_DIR"
printf 'LinkPlayer removed. Installed dependencies were left in place.\n'
