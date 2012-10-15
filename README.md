RasPyPlayer
===========

A simple media player for the Raspberry Pi, written in Python 3 and using the omxplayer backend.

Installation
------------

First you have to clone or download this repo in you /home/pi folder.

Then you have to run install.sh script to create the symbolic link in /usr/local/bin for RasPyPlayer. It will ask you for the sudo password once.

Finally you have to set the PATH variable in the RasPyPlayer.py file to your root folder containing your medias :

    #PATH="/home/pi"
    PATH="/home/pi/link_to_SAN"

