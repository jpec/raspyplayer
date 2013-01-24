#!/bin/sh
nano ./raspyplayer/DEBIAN/control
cp RasPyPlayer.py ./raspyplayer/usr/local/bin/raspyplayer
cp raspyplayer.conf ./raspyplayer/etc/raspyplayer.conf
cp raspyplayer.png ./raspyplayer/usr/share/pixmaps/raspyplayer.png
cp raspyplayer.desktop ./raspyplayer/usr/share/applications/raspyplayer.desktop
chmod a+rw ./raspyplayer/etc/raspyplayer.conf
chmod a+x ./raspyplayer/usr/local/bin/raspyplayer
dpkg-deb -b raspyplayer
echo "FIN !!!"
