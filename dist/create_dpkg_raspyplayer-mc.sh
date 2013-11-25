#!/bin/sh
DEBROOT="./debian-pkg/raspyplayer-mc"
SRCROOT="../src"
ARTROOT="../art"

echo "Creating Debian's package..."
nano $DEBROOT/DEBIAN/control
cp $SRCROOT/raspyplayer-mc.py $DEBROOT/usr/bin/raspyplayer-mc
cp $ARTROOT/raspyplayer-mc.png $DEBROOT/usr/share/pixmaps/raspyplayer-mc.png
cp $SRCROOT/raspyplayer-mc.desktop $DEBROOT/usr/share/applications/raspyplayer-mc.desktop
chmod a+x $DEBROOT/usr/bin/raspyplayer-mc
dpkg-deb -b debian-pkg/raspyplayer-mc

echo "Done !!!"
