#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# raspyplayer-lite.py - Video player designed for Raspberry Pi.
#-------------------------------------------------------------------------#
PROGRAM = 'Raspyplayer Lite'
VERSION = 'v0.2'
#-------------------------------------------------------------------------#
# Author : Julien Pecqueur (JPEC)
# Email : jpec@julienpecqueur.net
# Site : http://raspyplayer.org
# Sources : https://github.com/jpec/RasPyPlayer
# Bugs : https://github.com/jpec/RasPyPlayer/issues
#
# License :
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.
#-------------------------------------------------------------------------#


#-------------------------------------------------------------------------#
# SETTINGS
#-------------------------------------------------------------------------#

# Files extensions for movies
F_TYPES = ['.avi', '.mpg', '.mp4', '.wmv', '.mkv']

# OMXplayer command (no subtitles)
OMXCMD1 = 'xterm -e omxplayer {0} \"{1}\"'

# OMXplayer command (with subtitles)
OMXCMD2 = 'xterm -e omxplayer {0} --subtitles \"{1}\" \"{2}\"'

# OMXplayer options
# -o : output [local|hdmi]
# -t : enable subtitles [on|off]
# --align : subtitles aligment [center|left|right]
OPTIONS = '-o local -t on --align center'

#-------------------------------------------------------------------------#
# CODE
#-------------------------------------------------------------------------#

from sys import argv
from os import system
from os.path import isfile
from os.path import basename
from tkinter import *
from tkinter.messagebox import showinfo
from tkinter.filedialog import askopenfilename
from tkinter.ttk import Button, Frame


def playScreen():
    
    """Draw a dark bg."""
    
    ps = Tk()
    ps.title("Playing...")
    ps.attributes('-fullscreen', True)
    ps.configure(bg='black')
    lb = Label(ps, text="Playing...", bg='black', fg='grey')
    lb.pack()
    ps.update_idletasks()
    return(ps)


def play(file):
    
    """Play a movie"""
    
    sub = file[0:-3] + "srt"
    if isfile(sub):
        cmd = OMXCMD2.format(OPTIONS, sub, file)
    else:
        cmd = OMXCMD1.format(OPTIONS, file)
    print(cmd)
    system(cmd)
    return(True)


class Player(object):


    def __init__(self, file):
        
        """Init of Player"""
        
        self.file = file
        self.ui = self.drawUi()
        self.refreshUi()
        self.ui.mainloop()
    

    def openFile(self):
        
        """Display a filechooser window"""
        
        file = askopenfilename(title="Select a movie…")
        if isfile(file) and len(file) > 4 \
           and file[-4 : len(file)] in F_TYPES:
            self.file = file
            self.log(file)
        else:
            self.file = None
            self.log("No file selected…")
        self.refreshUi()


    def playFile(self):
        
        """Play a file"""
        
        self.log("Playing {}…".format(self.getName()))
        ps = playScreen()
        play(self.file)
        ps.destroy()
        
        
    def displayHelp(self):
        
        """Display help"""
        
        msg = "{} {}\n"
        msg += "--\n"
        msg += "Author: Julien Pecqueur\n"
        msg += "Home: http://julienpecqueur.net\n"
        msg += "Email: jpec@julienpecqueur.net\n"
        msg += "--\n"
        msg += "<o> open a movie\n"
        msg += "<Enter> play the movie\n"
        msg += "<F1> display help\n"
        msg = msg.format(PROGRAM, VERSION)
        showinfo("Help", msg)

        
    def getName(self):
        
        """Return name of the file"""
        
        if self.file:
            return(basename(self.file))
        else:
            return(None)

        
    def log(self, msg):
        
        """Append log in status bar"""
        
        self.ui.sb.log.configure(text="> {0}".format(msg))


    def evtPlay(self, evt):
        
        """Event bouton Play"""
        
        if self.file:
            self.playFile()

        
    def evtOpen(self, evt):
        
        """Event bouton Open"""
        
        self.openFile()

        
    def evtHelp(self, evt):
        
        """Event bouton Help"""
        
        self.displayHelp()

        
    def refreshUi(self):
        
        """Refresh the main window"""
        
        if self.file:
            # set title
            self.ui.title("{0} {1} - {2}".format(PROGRAM, VERSION,
                                                 self.getName()))
            # toggle play button
            self.ui.tb.b_play.configure(state=NORMAL)
            # display file info
            self.ui.mf.file.configure(text=self.getName())
            self.log("Ready to play…")
        else:
            # set title
            self.ui.title("{0} {1}".format(PROGRAM, VERSION))
            # toggle play button
            self.ui.tb.b_play.configure(state=DISABLED)
            # display file info
            self.ui.mf.file.configure(text="No file")
            self.log("No file selected…")


    def drawUi(self):
        
        """Draw the main window"""
        
        ui = Tk()
        ui.title("{0} {1}".format(PROGRAM, VERSION))
        # toolbar
        ui.tb = Frame(ui)
        ui.tb.pack(anchor='nw')
        ui.tb.b_open = Button(ui.tb, text="Open", command=self.openFile)
        ui.tb.b_open.grid(row=1, column=1, padx=2, pady=2)
        ui.tb.b_play = Button(ui.tb, text="Play", command=self.playFile)
        ui.tb.b_play.grid(row=1, column=2, padx=2, pady=2)
        ui.tb.b_help = Button(ui.tb, text="Help", command=self.displayHelp)
        ui.tb.b_help.grid(row=1, column=3, padx=2, pady=2)
        # file frame
        ui.mf = Frame(ui)
        ui.mf.pack(expand=True, fill='both')
        ui.mf.lbl = Label(ui.mf, text="Movie:")
        ui.mf.lbl.grid(row=1, column=1, padx=2, pady=2)
        ui.mf.file = Label(ui.mf)
        ui.mf.file.grid(row=1, column=2, padx=2, pady=2)
        # statusbar
        ui.sb = Frame(ui)
        ui.sb.pack(anchor='sw')
        ui.sb.log = Label(ui.sb)
        ui.sb.log.pack(expand=True, fill='both')
        # bindings
        ui.bind("<o>", self.evtOpen)
        ui.bind("<Return>", self.evtPlay)
        ui.bind("<F1>", self.evtHelp)
        return(ui)

# Main program
if len(argv) > 1:
    for p in argv:
        if isfile(p) and p[-4:] in F_TYPES:
            # param is a readable file
            player = Player(p)
else:
    player = Player(None)

