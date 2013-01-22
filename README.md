RasPyPlayer
===========

A simple media player for the Raspberry Pi, written in Python 3 and using the omxplayer backend.

http://raspyplayer.org

Installation (Raspbian)
-----------------------

Download the Raspbian package on this page (raspyplayer.deb) and save it on your Pi. 

Use the following command to install RasPyPlayer:

    sudo dpkg -i raspyplayer.deb

Configuration :
---------------

You can configure RasPyPlayer by editing the configuration file:

    sudo nano /etc/raspyplayer.conf

Mount SMB Folder at /media/nas
--------------------------------

Add the following line in your /etc/rc.local:

    mount -t cifs //nashostname/nasvolume/ -o username=<smb username>,password=<smb password> /media/nas -o iocharset=utf8

First launch of RasPyPlayer
---------------------------

You can find the RasPyPlayer program in the LXDE menu. You need to click on "SCAN" to refresh you movies database. You can also launch it from command line:

    raspyplayer



