pkgname=linkplayer
pkgver=1.0.0
pkgrel=1
pkgdesc='Lightweight GUI for playing and downloading supported video links'
arch=('any')
license=('GPL-3.0-or-later')
depends=('python' 'tk' 'mpv' 'yt-dlp' 'ffmpeg')
source=('linkplayer.py' 'linkplayer.desktop')
sha256sums=('SKIP' 'SKIP')

package() {
  install -Dm755 "$srcdir/linkplayer.py" "$pkgdir/usr/share/linkplayer/linkplayer.py"
  install -Dm644 "$srcdir/linkplayer.desktop" "$pkgdir/usr/share/applications/linkplayer.desktop"
  install -d "$pkgdir/usr/bin"
  printf '%s\n' '#!/usr/bin/env sh' 'exec python3 /usr/share/linkplayer/linkplayer.py "$@"' > "$pkgdir/usr/bin/linkplayer"
  chmod 755 "$pkgdir/usr/bin/linkplayer"
}
