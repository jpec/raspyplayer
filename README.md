Raspyplayer Media Center & Raspyplayer Lite
===========================================

Media Center and Video Player for the Raspberry Pi, written in Python 3 and using the omxplayer backend.

http://raspyplayer.org

Installation Raspyplayer Media Center (Raspbian)
------------------------------------------------

Download the Raspbian package (raspyplayer-mc.deb) and save it on your Pi. 

Use the following command to install Raspyplayer Media Center :

    sudo dpkg -i raspyplayer-mc.deb

Installation Raspyplayer Lite (Raspbian)
----------------------------------------

Download the Raspbian package (raspyplayer-lite.deb) and save it on your Pi. 

Use the following command to install Raspyplayer Lite :

    sudo dpkg -i raspyplayer-lite.deb


Installation (Archlinux)
------------------------

You can install RasPyPlayer via AUR.

Mount SMB Folder at /media/nas
--------------------------------

Add the following line in your /etc/rc.local:

    mount -t cifs //nashostname/nasvolume/ -o username=<smb username>,password=<smb password> /media/nas -o iocharset=utf8

First launch of Raspyplayer
---------------------------

You can find the RasPyPlayer programs in the menu. You need to click on "Scan" to refresh you movies database. 



