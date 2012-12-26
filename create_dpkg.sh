#!/bin/sh
nano ./raspyplayer/DEBIAN/control
cp RasPyPlayer.py ./raspyplayer/usr/local/bin/RasPyPlayer
cp raspyplayer.png ./raspyplayer/usr/share/pixmaps/raspyplayer.png
cp raspyplayer.desktop ./raspyplayer/usr/share/applications/raspyplayer.desktop
dpkg-deb -b raspyplayer
echo "FIN !!!"