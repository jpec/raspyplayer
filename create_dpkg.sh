#!/bin/sh
nano ./raspyplayer/DEBIAN/control
cp RasPyPlayer.py ./raspyplayer/usr/local/bin/RasPyPlayer
cp raspyplayer.png ./raspyplayer/usr/share/pixmaps/raspyplayer.png
cp RasPyPlayer.desktop ./raspyplayer/usr/share/applications/RasPyPlayer.desktop
dpkg-deb -b raspyplayer
echo "FIN !!!"
