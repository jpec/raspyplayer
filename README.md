RasPyPlayer
===========

A simple media player for the Raspberry Pi, written in Python 3 and using the omxplayer backend.

http://raspyplayer.org

Installation (Raspbian)
-----------------------

Download the Raspbian package on this page (raspyplayer.deb) and save it on your Pi. 
Use the following command to install RasPyPlayer :

    sudo dpkg -i raspyplayer.deb

Configuration
-------------

Use the following command to open the Python program : 

    sudo nano /usr/local/bin/RasPyPlayer

You have to adjust the following options :

    PATH - you need to replace "/home/pi/nas" by the path to your medias folder.

    EXC - You can add in the list the folders you don't want to index.

    LANG - If you are french, you can replace "EN" by "FR".


Mount SMB Folder at /home/pi/nas
--------------------------------

Add the following line in your /etc/rc.local:

    mount -t cifs //192.168.0.4/Volume_1/ -o username=<smb username>,password=<smb password> nas -o iocharset=utf8,file_mode=0777,dir_mode=0777

First launch of RasPyPlayer
---------------------------

You can find the RasPyPlayer program in the LXDE menu. You need to click on "SCAN" to refresh you movies database.


Installation (old way)
----------------------

First you have to clone or download this repo in you /home/pi folder.

Then you have to run install.sh script to create the executable in /usr/local/bin for RasPyPlayer. It will ask you for the sudo password. It will copy the RasPyPlayer icon in /usr/share/pixmaps.

Finally you have to set the PATH variable in the RasPyPlayer.py file to your root folder containing your medias :

    #PATH="/home/pi"
    PATH="/home/pi/nas"

Uninstallation (old way)
------------------------

Execute the uninstall.sh script.
