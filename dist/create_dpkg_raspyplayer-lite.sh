#!/bin/sh
DEBROOT="./debian-pkg/raspyplayer-lite"
SRCROOT="../src"
ARTROOT="../art"

echo "Creating Debian's package..."
nano $DEBROOT/DEBIAN/control
cp $SRCROOT/raspyplayer-lite.py $DEBROOT/usr/bin/raspyplayer-lite
cp $ARTROOT/raspyplayer-lite.png $DEBROOT/usr/share/pixmaps/raspyplayer-lite.png
cp $SRCROOT/raspyplayer-lite.desktop $DEBROOT/usr/share/applications/raspyplayer-lite.desktop
chmod a+x $DEBROOT/usr/bin/raspyplayer-lite
dpkg-deb -b debian-pkg/raspyplayer-lite

echo "Done !!!"
