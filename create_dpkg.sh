#!/bin/sh
echo "Creating Debian's package..."
nano ./raspyplayer/DEBIAN/control
cp RasPyPlayer.py ./raspyplayer/usr/local/bin/raspyplayer
cp raspyplayer.conf ./raspyplayer/etc/raspyplayer.conf
cp raspyplayer.png ./raspyplayer/usr/share/pixmaps/raspyplayer.png
cp raspyplayer.desktop ./raspyplayer/usr/share/applications/raspyplayer.desktop
chmod a+rw ./raspyplayer/etc/raspyplayer.conf
chmod a+x ./raspyplayer/usr/local/bin/raspyplayer
dpkg-deb -b raspyplayer
echo "Creating Archlinux's package..."
nano ./raspyplayer-aur/PKGBUILD
mkdir ./raspyplayer-aur/raspyplayer-vx.x
cp RasPyPlayer.py ./raspyplayer-aur/raspyplayer-vx.x/
cp raspyplayer.conf ./raspyplayer-aur/raspyplayer-vx.x/
cp raspyplayer.png ./raspyplayer-aur/raspyplayer-vx.x/
cp raspyplayer.desktop ./raspyplayer-aur/raspyplayer-vx.x/
chmod a+rw ./raspyplayer-aur/raspyplayer-vx.x/raspyplayer.conf
chmod a+x ./raspyplayer-aur/raspyplayer-vx.x/RasPyPlayer.py
cd ./raspyplayer-aur/
echo "Please rename raspyplayer-vx.x and tar -cf raspyplayer-vx.x.tar.gz raspyplayer-vx.x and upload it on ftp."
