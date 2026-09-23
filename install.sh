#!/usr/bin/env bash
set -euo pipefail

SOURCE_DIR="$(cd -- "$(dirname -- "${BASH_SOURCE[0]}")" && pwd)"
APP_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/linkplayer"
BIN_DIR="${HOME}/.local/bin"
APP_MENU_DIR="${XDG_DATA_HOME:-$HOME/.local/share}/applications"

for command in python3; do
    if ! command -v "$command" >/dev/null 2>&1; then
        printf 'Missing dependency: %s\nInstall it with: sudo pacman -S python tk mpv yt-dlp ffmpeg\n' "$command" >&2
        exit 1
    fi
done

mkdir -p "$APP_DIR" "$BIN_DIR" "$APP_MENU_DIR"
install -m 755 "$SOURCE_DIR/linkplayer.py" "$APP_DIR/linkplayer.py"
install -m 644 "$SOURCE_DIR/README.md" "$APP_DIR/README.md"
cat > "$BIN_DIR/linkplayer" <<EOF
#!/usr/bin/env sh
exec python3 "$APP_DIR/linkplayer.py" "\$@"
EOF
chmod 755 "$BIN_DIR/linkplayer"
sed "s|^Exec=linkplayer$|Exec=$BIN_DIR/linkplayer|" "$SOURCE_DIR/linkplayer.desktop" > "$APP_MENU_DIR/linkplayer.desktop"

printf 'LinkPlayer installed. It should now appear in your application menu.\n'
if [[ ":${PATH}:" != *":${BIN_DIR}:"* ]]; then
    printf 'Note: %s is not on PATH; the menu entry uses its full path, so it will still launch.\n' "$BIN_DIR"
fi
printf 'Install dependencies with: sudo pacman -S tk mpv yt-dlp ffmpeg\n'
