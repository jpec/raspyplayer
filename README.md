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

Options:

    # PATH - Root directory of the movies
	PATH=/media/nas

	# EXC - Exclude theses directories from movies search
	EXC=Rep1
	EXC=Rep2

	# EXT - Extensions of movies
	EXT=.avi
	EXT=.mpg
	EXT=.mp4
	EXT=.wmv
	EXT=.mkv

	# DB - Database file name
	DB=.raspyplayer.sqlite3

	# OMXSRT - Omxplayer version can handle subtitles
	OMXSRT=1


Mount SMB Folder at /media/nas
--------------------------------

Add the following line in your /etc/rc.local:

    mount -t cifs //nashostname/nasvolume/ -o username=<smb username>,password=<smb password> /media/nas -o iocharset=utf8

First launch of RasPyPlayer
---------------------------

You can find the RasPyPlayer program in the LXDE menu. You need to click on "SCAN" to refresh you movies database. You can also launch it from command line:

    raspyplayer



