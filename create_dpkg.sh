#!/bin/sh
echo "Creating Debian's package..."
nano ./raspyplayer/DEBIAN/control
cp RasPyPlayer.py ./raspyplayer/usr/local/bin/raspyplayer
cp raspyplayer.png ./raspyplayer/usr/share/pixmaps/raspyplayer.png
cp raspyplayer.desktop ./raspyplayer/usr/share/applications/raspyplayer.desktop
chmod a+x ./raspyplayer/usr/local/bin/raspyplayer
dpkg-deb -b raspyplayer
