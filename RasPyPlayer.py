#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# RasPyPlayer.py - Movies player originally designed for Raspberry Pi.
#-------------------------------------------------------------------------#
VERSION = "2.5-dev"
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
# PARAMS
#-------------------------------------------------------------------------#

# DEBUG - Debug mode (False / True) :
DEBUG = False

#-------------------------------------------------------------------------#
# MODULES
#-------------------------------------------------------------------------#

from os import listdir
from os import system
from os.path import isdir
from os.path import isfile
from os.path import basename
from os.path import expanduser
from sqlite3 import connect
from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import StringVar
from tkinter import EXTENDED
from tkinter import BOTH
from tkinter import W
from tkinter import Y
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import END
from tkinter import NORMAL
from tkinter import DISABLED
from tkinter import messagebox
from tkinter.font import Font

#-------------------------------------------------------------------------#
# FUNCTIONS
#-------------------------------------------------------------------------#

def scanFiles(db, cfg, path):

    """Look for movies in path to add in DB."""

    if DEBUG:
        print("Scan {0}".format(path))
    for file in listdir(path):
        filepath = path+"/"+file
        if len(file) > 4 and file[-4: len(file)] in cfg.EXT and file[0:1] != ".":
            # File
            db.addMovie(basename(file), filepath)
        elif isdir(filepath) and not file in cfg.EXC \
            and file[0:1] != ".":
            # Directory
            scanFiles(db, cfg, filepath)

#-------------------------------------------------------------------------#

def lst2str(l):

    """Transform list to string."""

    s = ""
    for i in l:
        s = s + i + ","
    if len(s) > 1 or s == ",":
        s = s[0:-1]
    return(s)

#-------------------------------------------------------------------------#

def str2lst(s):

    """Transform string to list."""

    l = s.split(',')
    return(l)

#-------------------------------------------------------------------------#

def error(msg):

    """Logging error messages"""

    print("[ERROR] {}".format(msg))

#-------------------------------------------------------------------------#

def getHelp():

    """Return help text"""

    msg = "RasPyPlayer, v{0}\n"
    msg += "Author : Julien Pecqueur (JPEC)\n"
    msg += "Mail : jpec@julienpecqueur.net\n"
    msg += "Home : http://raspyplayer.org\n"
    msg += "License : GPL\n"
    msg += "\n"
    msg += "Keyboard shortcuts :\n"
    msg += "<F1> HELP\n"
    msg += "<F2> CONFIG\n"
    msg += "<F3> SEARCH\n"
    msg += "<F5> SCAN\n"
    msg += "<F12> QUIT\n"
    return(msg.format(VERSION))

#-------------------------------------------------------------------------#

def playScreen():

    """Draw a dark bg."""

    print("*** Drawing the PlayScreen ***")
    ps = Tk()
    ps.title("Playing...")
    ps.attributes('-fullscreen', True)
    ps.configure(bg='black')
    lb = Label(ps, text="Playing...", bg='black', fg='grey')
    lb.pack()
    ps.update_idletasks()
    return(ps)

#-------------------------------------------------------------------------#
# CLASSES
#-------------------------------------------------------------------------#

class Config(object):

    """Configuration class"""

    def __init__(self):

        """Initialisation of the config object"""

        self.CONF = "{0}/.raspyplayer.conf".format(expanduser('~'))
        # Values loaded from CONF file
        self.clearConf()
        # Values hard coded
        self.MPLRCMD = 'xterm -e mplayer -fs \"{0}\"'
        self.OMXCMD1 = 'xterm -e omxplayer {0} -o {1} \"{2}\"'
        self.OMXCMD2 = 'xterm -e omxplayer {0} -o {1} --subtitles \"{2}\" \"{3}\"'
        # DB*** - SQL requests
        self.DBADD = self.initDbAdd()
        self.DBALL = self.initDbAll()
        self.DBSRC = self.initDbSrc()
        self.DBDRP = self.initDbDrp()
        self.DBCRT = self.initDbCrt()

    #---------------------------------------------------------------------#

    def clearConf(self):

        """Clear conf settings"""

        self.PATH = None
        self.EXC = []
        self.EXT = []
        self.DB = None
        self.URL1 = None
        self.URL2 = None
        self.URL3 = None
        self.URL4 = None
        self.URL5 = None
        self.URL1L = 'URL1'
        self.URL2L = 'URL2'
        self.URL3L = 'URL3'
        self.URL4L = 'URL4'
        self.URL5L = 'URL5'
        self.OUT = 'local'
        self.OPT = '-t on --align center --no-ghost-box'

    #---------------------------------------------------------------------#

    def readConf(self):

        """Read the CONF file"""

        if isfile(self.CONF):
            self.clearConf()
            f = open(self.CONF, 'r')
            for l in f.readlines():
                l = l.replace("\n", "")
                if len(l) >= 3 and l[0:3] == "DB=":
                    self.DB = l[3:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 4 and l[0:4] == "EXC=":
                    self.EXC.append(l[4:len(l)])
                    if DEBUG:
                        print(l)
                elif len(l) >= 4 and l[0:4] == "EXT=":
                    self.EXT.append(l[4:len(l)])
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "PATH=":
                    self.PATH = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "URL1=":
                    self.URL1 = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "URL2=":
                    self.URL2 = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "URL3=":
                    self.URL3 = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "URL4=":
                    self.URL4 = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 5 and l[0:5] == "URL5=":
                    self.URL5 = l[5:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 6 and l[0:6] == "URL1L=":
                    self.URL1L = l[6:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 6 and l[0:6] == "URL2L=":
                    self.URL2L = l[6:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 6 and l[0:6] == "URL3L=":
                    self.URL3L = l[6:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 6 and l[0:6] == "URL4L=":
                    self.URL4L = l[6:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 6 and l[0:6] == "URL5L=":
                    self.URL5L = l[6:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 4 and l[0:4] == "OUT=":
                    self.OUT = l[4:len(l)]
                    if DEBUG:
                        print(l)
                elif len(l) >= 4 and l[0:4] == "OPT=":
                    self.OPT = l[4:len(l)]
                    if DEBUG:
                        print(l)
            f.close()
            return(True)
        else:
            return(False)

    #---------------------------------------------------------------------#

    def checkConf(self):

        """Check the CONF"""

        res = True
        if not self.DB:
            self.errorVar("Database name", "n/a")
            res = False
        if not self.PATH:
            self.errorVar("Root directory", "n/a")
            res = False
        return(res)

    #---------------------------------------------------------------------#

    def errorVar(self, var, val):

        """Ask user to set correct setting"""

        msg = "{0} is not correct :\n'{1}'\nPlease set it in Config"
        messagebox.showerror("WARNING !", msg.format(var, str(val)))
        return(True)

    #---------------------------------------------------------------------#

    def useOmx(self):

        """We use OMXPLAYER ?"""

        if isfile('/usr/bin/omxplayer'):
            return(True)
        else:
            return(False)

    #---------------------------------------------------------------------#

    def initDbAdd(self):

        """Initialisation of the DBADD request"""

        res = "INSERT INTO files VALUES (?, ?)"
        return(res)

    #---------------------------------------------------------------------#

    def initDbSrc(self):

        """Initialisation of the DBSRC request"""

        res = "SELECT * FROM files WHERE file LIKE ? ORDER BY file"
        return(res)

    #---------------------------------------------------------------------#

    def initDbAll(self):

        """Initialisation of the DBALL request"""

        res = "SELECT * FROM files ORDER BY file"
        return(res)

    #---------------------------------------------------------------------#

    def initDbDrp(self):

        """Initialisation of the DBDRP request"""

        res = "DROP TABLE files"
        return(res)

    #---------------------------------------------------------------------#

    def initDbCrt(self):

        """Initialisation of the DBCRT request"""

        res = "CREATE TABLE files (file, path)"
        return(res)

    #---------------------------------------------------------------------#

    def display(self, root):

        """Display the setting window"""

        if self.createGui():
            self.player = root
            self.fill()
            self.root.mainloop()
        return(True)

    #---------------------------------------------------------------------#

    def fill(self):

        """Fill the setting window"""

        if self.PATH:
            self.ui_path.insert(0, self.PATH)
        self.ui_exc.insert(0, lst2str(self.EXC))
        self.ui_ext.insert(0, lst2str(self.EXT))
        if self.DB:
            self.ui_db.insert(0, self.DB)
        if self.URL1:
            self.ui_url1.insert(0, self.URL1)
        if self.URL2:
            self.ui_url2.insert(0, self.URL2)
        if self.URL3:
            self.ui_url3.insert(0, self.URL3)
        if self.URL4:
            self.ui_url4.insert(0, self.URL4)
        if self.URL5:
            self.ui_url5.insert(0, self.URL5)
        self.ui_url1l.insert(0, self.URL1L)
        self.ui_url2l.insert(0, self.URL2L)
        self.ui_url3l.insert(0, self.URL3L)
        self.ui_url4l.insert(0, self.URL4L)
        self.ui_url5l.insert(0, self.URL5L)
        self.ui_out.insert(0, self.OUT)
        self.ui_opt.insert(0, self.OPT)

    #---------------------------------------------------------------------#

    def reload(self):

        """Load the conf from the setting window"""

        self.PATH = self.ui_path.get()
        self.EXC = str2lst(self.ui_exc.get())
        self.EXT = str2lst(self.ui_ext.get())
        self.DB = self.ui_db.get()
        self.URL1 = self.ui_url1.get()
        self.URL2 = self.ui_url2.get()
        self.URL3 = self.ui_url3.get()
        self.URL4 = self.ui_url4.get()
        self.URL5 = self.ui_url5.get()
        self.URL1L = self.ui_url1l.get()
        self.URL2L = self.ui_url2l.get()
        self.URL3L = self.ui_url3l.get()
        self.URL4L = self.ui_url4l.get()
        self.URL5L = self.ui_url5l.get()
        self.OUT = self.ui_out.get()
        self.OPT = self.ui_opt.get()

    #---------------------------------------------------------------------#

    def save(self):

        """Save the config"""

        print("*** Saving the configuration ***")
        self.reload()
        f = open(self.CONF, 'w')
        line = "DB=" + self.DB
        f.write(line+"\n")
        for i in self.EXC:
            line = "EXC=" + i
            f.write(line+"\n")
        for i in self.EXT:
            line = "EXT=" + i
            f.write(line+"\n")
        line = "PATH=" + self.PATH
        f.write(line+"\n")
        line = "URL1=" + self.URL1
        f.write(line+"\n")
        line = "URL2=" + self.URL2
        f.write(line+"\n")
        line = "URL3=" + self.URL3
        f.write(line+"\n")
        line = "URL4=" + self.URL4
        f.write(line+"\n")
        line = "URL5=" + self.URL5
        f.write(line+"\n")
        line = "URL1L=" + self.URL1L
        f.write(line+"\n")
        line = "URL2L=" + self.URL2L
        f.write(line+"\n")
        line = "URL3L=" + self.URL3L
        f.write(line+"\n")
        line = "URL4L=" + self.URL4L
        f.write(line+"\n")
        line = "URL5L=" + self.URL5L
        f.write(line+"\n")
        line = "OUT=" + self.OUT
        f.write(line+"\n")
        line = "OPT=" + self.OPT
        f.write(line+"\n")
        f.close()
        if self.checkConf():
            self.toggleUrl(self.player)
            self.root.destroy()
    #---------------------------------------------------------------------#

    def toggleUrl(self, player):

        """Enable / disable url buttons"""

        if self.URL1:
            s = NORMAL
            player.URL1L.set(self.URL1L)
        else:
            s = DISABLED
            player.URL1L.set("N/A")
        player.ui_buturl1.configure(state=s)
        player.ui_buturl1.update_idletasks()
        if self.URL2:
            s = NORMAL
            player.URL2L.set(self.URL2L)
        else:
            s = DISABLED
            player.URL2L.set("N/A")
        player.ui_buturl2.configure(state=s)
        player.ui_buturl2.update_idletasks()
        if self.URL3:
            s = NORMAL
            player.URL3L.set(self.URL3L)
        else:
            s = DISABLED
            player.URL3L.set("N/A")
        player.ui_buturl3.configure(state=s)
        player.ui_buturl3.update_idletasks()
        if self.URL4:
            s = NORMAL
            player.URL4L.set(self.URL4L)
        else:
            s = DISABLED
            player.URL4L.set("N/A")
        player.ui_buturl4.configure(state=s)
        player.ui_buturl4.update_idletasks()
        if self.URL5:
            s = NORMAL
            player.URL5L.set(self.URL5L)
        else:
            s = DISABLED
            player.URL5L.set("N/A")
        player.ui_buturl5.configure(state=s)
        player.ui_buturl5.update_idletasks()
        # Refresh
        player.root.update_idletasks()

    #---------------------------------------------------------------------#

    def createGui(self):

        """Create the GUI for Config"""

        print("*** Creating Configuration GUI ***")
        self.root = Tk()
        self.root.title("Configuration")
        self.root.attributes('-topmost', True)
        font = Font(self.root, size=12, family='Sans')
        # Middle Frame (config group)
        self.ui_midframe = Frame(self.root, borderwidth=2)
        self.ui_midframe.pack(fill=BOTH, expand=1)
        # PATH
        self.ui_pathlbl = Label(self.ui_midframe, text="Movies root folder",
            justify=LEFT, anchor=W, font=font)
        self.ui_pathlbl.grid(row=0, column=0, padx=2, pady=2)
        self.ui_path = Entry(self.ui_midframe, font=font)
        self.ui_path.grid(row=0, column=1, padx=2, pady=2)
        # EXC
        self.ui_exclbl = Label(self.ui_midframe, text="Directories to exclude",
            justify=LEFT, anchor=W, font=font)
        self.ui_exclbl.grid(row=1, column=0, padx=2, pady=2)
        self.ui_exc = Entry(self.ui_midframe, font=font)
        self.ui_exc.grid(row=1, column=1, padx=2, pady=2)
        # EXT
        self.ui_extlbl = Label(self.ui_midframe, text="Movies extensions",
            justify=LEFT, anchor=W, font=font )
        self.ui_extlbl.grid(row=2, column=0, padx=2, pady=2)
        self.ui_ext = Entry(self.ui_midframe, font=font)
        self.ui_ext.grid(row=2, column=1, padx=2, pady=2)
        # DB
        self.ui_dblbl = Label(self.ui_midframe, text="Database name",
            justify=LEFT, anchor=W, font=font )
        self.ui_dblbl.grid(row=3, column=0, padx=2, pady=2)
        self.ui_db = Entry(self.ui_midframe, font=font)
        self.ui_db.grid(row=3, column=1, padx=2, pady=2)
        # OUT
        self.ui_outlbl = Label(self.ui_midframe, text="Audio output (local/hdmi)",
            justify=LEFT, anchor=W, font=font )
        self.ui_outlbl.grid(row=4, column=0, padx=2, pady=2)
        self.ui_out = Entry(self.ui_midframe, font=font)
        self.ui_out.grid(row=4, column=1, padx=2, pady=2)
        # OPT
        self.ui_optlbl = Label(self.ui_midframe, text="Omxplayer extra options",
            justify=LEFT, anchor=W, font=font )
        self.ui_optlbl.grid(row=5, column=0, padx=2, pady=2)
        self.ui_opt = Entry(self.ui_midframe, font=font)
        self.ui_opt.grid(row=5, column=1, padx=2, pady=2)
        # URL1L
        self.ui_url1llbl = Label(self.ui_midframe, text="Url 1 name",
            justify=LEFT, anchor=W, font=font )
        self.ui_url1llbl.grid(row=6, column=0, padx=2, pady=2)
        self.ui_url1l = Entry(self.ui_midframe, font=font)
        self.ui_url1l.grid(row=6, column=1, padx=2, pady=2)
        # URL1
        self.ui_url1lbl = Label(self.ui_midframe, text="Url 1",
            justify=LEFT, anchor=W, font=font )
        self.ui_url1lbl.grid(row=7, column=0, padx=2, pady=2)
        self.ui_url1 = Entry(self.ui_midframe, font=font)
        self.ui_url1.grid(row=7, column=1, padx=2, pady=2)
        # URL2L
        self.ui_url2llbl = Label(self.ui_midframe, text="Url 2 name",
            justify=LEFT, anchor=W, font=font )
        self.ui_url2llbl.grid(row=8, column=0, padx=2, pady=2)
        self.ui_url2l = Entry(self.ui_midframe, font=font)
        self.ui_url2l.grid(row=8, column=1, padx=2, pady=2)
        # URL2
        self.ui_url2lbl = Label(self.ui_midframe, text="Url 2",
            justify=LEFT, anchor=W, font=font )
        self.ui_url2lbl.grid(row=9, column=0, padx=2, pady=2)
        self.ui_url2 = Entry(self.ui_midframe, font=font)
        self.ui_url2.grid(row=9, column=1, padx=2, pady=2)
        # URL3L
        self.ui_url3llbl = Label(self.ui_midframe, text="Url 3 name",
            justify=LEFT, anchor=W, font=font )
        self.ui_url3llbl.grid(row=10, column=0, padx=2, pady=2)
        self.ui_url3l = Entry(self.ui_midframe, font=font)
        self.ui_url3l.grid(row=10, column=1, padx=2, pady=2)
        # URL3
        self.ui_url3lbl = Label(self.ui_midframe, text="Url 3",
            justify=LEFT, anchor=W, font=font )
        self.ui_url3lbl.grid(row=11, column=0, padx=2, pady=2)
        self.ui_url3 = Entry(self.ui_midframe, font=font)
        self.ui_url3.grid(row=11, column=1, padx=2, pady=2)
        # URL4L
        self.ui_url4llbl = Label(self.ui_midframe, text="Url 4 name",
            justify=LEFT, anchor=W, font=font )
        self.ui_url4llbl.grid(row=12, column=0, padx=2, pady=2)
        self.ui_url4l = Entry(self.ui_midframe, font=font)
        self.ui_url4l.grid(row=12, column=1, padx=2, pady=2)
        # URL4
        self.ui_url4lbl = Label(self.ui_midframe, text="Url 4",
            justify=LEFT, anchor=W, font=font )
        self.ui_url4lbl.grid(row=13, column=0, padx=2, pady=2)
        self.ui_url4 = Entry(self.ui_midframe, font=font)
        self.ui_url4.grid(row=13, column=1, padx=2, pady=2)
        # URL5L
        self.ui_url5llbl = Label(self.ui_midframe, text="Url 5 name",
            justify=LEFT, anchor=W, font=font )
        self.ui_url5llbl.grid(row=14, column=0, padx=2, pady=2)
        self.ui_url5l = Entry(self.ui_midframe, font=font)
        self.ui_url5l.grid(row=14, column=1, padx=2, pady=2)
        # URL5
        self.ui_url5lbl = Label(self.ui_midframe, text="Url 5",
            justify=LEFT, anchor=W, font=font )
        self.ui_url5lbl.grid(row=15, column=0, padx=2, pady=2)
        self.ui_url5 = Entry(self.ui_midframe, font=font)
        self.ui_url5.grid(row=15, column=1, padx=2, pady=2)
        # Bottom Frame (buttons group)
        self.ui_botframe = Frame(self.root, borderwidth=2)
        self.ui_botframe.pack(anchor='s')
        # Button Save
        self.ui_butsave = Button(self.ui_botframe, text="Save",
            command=self.save, font=font)
        self.ui_butsave.grid(row=1, column=0, padx=2, pady=2)
        # Button Close
        self.ui_butquit = Button(self.ui_botframe, text="Close",
            command=self.root.destroy, font=font)
        self.ui_butquit.grid(row=1, column=1, padx=2, pady=2)
        # Window position
        self.root.update_idletasks()
        w = self.root.winfo_reqwidth()
        h = self.root.winfo_reqheight()
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
        self.root.minsize(w, h)
        self.root.maxsize(w, h)
        return(True)

    #---------------------------------------------------------------------#

#-------------------------------------------------------------------------#

class Db(object):

    """DataBase class"""

    def __init__(self, cfg):

        """Initialisation of the DB object"""

        self.cfg = cfg
        self.db = "{0}/{1}".format(expanduser('~'), cfg.DB)
        self.con = None
        self.cur = None
        self.new = False

    #---------------------------------------------------------------------#

    def openDb(self):

        """Open the DB"""

        print("*** DB - Opening the database ***")
        new = False
        if not isfile(self.db):
            new = True
        self.con = connect(self.db)
        self.cur = self.con.cursor()
        if new:
            self.createDb()
        return(True)

    #---------------------------------------------------------------------#

    def createDb(self):

        """Create the DB"""

        print("*** DB - Creating the database ***")
        self.execSql(self.cfg.DBCRT, False)
        self.commitDb()
        return(True)

    #---------------------------------------------------------------------#

    def dropDb(self):

        """Drop the DB"""

        print("*** DB - Dropping the database ***")
        self.execSql(self.cfg.DBDRP, False)
        return(True)

    #---------------------------------------------------------------------#

    def initDb(self):

        """Initialisation of the DB"""

        print("*** DB - Initializing the database ***")
        self.dropDb()
        self.createDb()
        return(True)

    #---------------------------------------------------------------------#

    def closeDb(self):

        """Close the DB"""

        print("*** DB - Closing the database ***")
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None
        return(True)

    #---------------------------------------------------------------------#

    def commitDb(self):

        """Commit"""

        print("*** DB - Commiting the database ***")
        self.con.commit()

    #---------------------------------------------------------------------#

    def execSql(self, sql, bind):

        """Execute a SQL statement in DB"""

        if sql:
            if bind:
                if DEBUG:
                    print(sql, bind)
                self.cur.execute(sql, bind)
            else:
                if DEBUG:
                    print(sql)
                self.cur.execute(sql)
            return(True)
        else:
            return(False)

    #---------------------------------------------------------------------#

    def getAllMovies(self):

        """Return all movies from DB"""

        files = {}
        self.execSql(self.cfg.DBALL, False)
        for file, path in self.cur:
            files[file] = path
        return(files)

    #---------------------------------------------------------------------#

    def getSrcMovies(self, src):

        """Return movies from DB with search pattern"""

        files = {}
        self.execSql(self.cfg.DBSRC, src)
        for file, path in self.cur:
            files[file] = path
        return(files)

    #---------------------------------------------------------------------#

    def addMovie(self, file, filepath):

        """Add a movie in DB"""

        self.execSql(self.cfg.DBADD, (file, filepath))
        return(True)

    #---------------------------------------------------------------------#

#-------------------------------------------------------------------------#

class Player(object):

    """Player class"""

    def __init__(self):

        """Initialisation of the Player object"""

        self.cfg = None
        self.db = None
        self.root = Tk()
        self.URL1L = StringVar(master=self.root)
        self.URL2L = StringVar(master=self.root)
        self.URL3L = StringVar(master=self.root)
        self.URL4L = StringVar(master=self.root)
        self.URL5L = StringVar(master=self.root)
        self.files = {}
        self.start()

    #---------------------------------------------------------------------#

    def start(self):

        """Start the Player"""

        print("*** Starting the Player ***")
        # Configuration
        self.cfg = Config()
        while not self.cfg.readConf() or not self.cfg.checkConf():
            self.displayConfig()
        if self.cfg.readConf() and self.cfg.checkConf():
            # Database
            self.db = Db(self.cfg)
            if self.db.openDb():
                self.display()
                return(True)
            else:
                error("Database not open")
                return(False)
        else:
            error("Cannot read configuration file")
            return(False)

    #---------------------------------------------------------------------#

    def stop(self):

        """Stop the Player"""

        msg = "Do you want to quit RasPyPlayer ?"
        if messagebox.askokcancel("RasPyPlayer", msg):
            print("*** Stopping the Player ***")
            self.db.closeDb()
            self.root.destroy()

    #---------------------------------------------------------------------#

    def scanDB(self):

        """Add movies in DB"""

        print("*** Adding movies in database")
        self.db.initDb()
        scanFiles(self.db, self.cfg, self.cfg.PATH)
        self.db.commitDb()
        return(True)

    #---------------------------------------------------------------------#

    def loadAllMovies(self):

        """Load movies from DB"""

        self.files = self.db.getAllMovies()
        return(True)

    #---------------------------------------------------------------------#

    def loadSrcMovies(self, src):

        """Load movies matching search pattern"""

        self.files = self.db.getSrcMovies(src)
        return(True)

    #---------------------------------------------------------------------#

    def play(self, url, file):

        """Play a movie"""

        print("Playing {}".format(file))
        if self.cfg.useOmx():
            if not url:
                sub = file[0:-3] + "srt"
                if isfile(sub):
                    cmd = self.cfg.OMXCMD2.format(self.cfg.OPT, self.cfg.OUT, sub, file)
                else:
                    cmd = self.cfg.OMXCMD1.format(self.cfg.OPT, self.cfg.OUT, file)
            else:
                cmd = self.cfg.OMXCMD1.format(self.cfg.OPT, self.cfg.OUT, file)
        else:
            cmd = self.cfg.MPLRCMD.format(file)
        if DEBUG:
            print(cmd)
        system(cmd)
        return(True)

    #---------------------------------------------------------------------#

    def displayHelp(self):

        """Display help"""

        messagebox.showinfo("Help...", getHelp())
        return(True)

    #---------------------------------------------------------------------#

    def displayConfig(self):

        """Display Config Window"""

        self.cfg.display(self)
        self.askToRefreshDataBase()
        return(True)

    #---------------------------------------------------------------------#

    def playSelection(self):

        """Play selected files"""

        sel = self.ui_files.curselection()
        ps = playScreen()
        for i in sel:
            f = self.ui_files.get(i)
            self.play(False, self.files[f])
        ps.destroy()
        return(True)

    #---------------------------------------------------------------------#

    def playUrl(self, url):

        """Play selected url"""

        ps = playScreen()
        self.play(True, url)
        ps.destroy()
        return(True)

    #---------------------------------------------------------------------#

    def display(self):

        """Display the player"""

        self.createGui()
        self.cfg.toggleUrl(self)
        self.askToRefreshDataBase()
        self.root.mainloop()

    #---------------------------------------------------------------------#

    def askToRefreshDataBase(self):

        """Ask to refresh database"""

        msg = "Do you want to refresh the movies database ?"
        if messagebox.askokcancel("RasPyPlayer", msg):
            self.refreshDataBase()
        else:
            self.refreshFilesList()
        return(True)

    #---------------------------------------------------------------------#

    def refreshDataBase(self):

        """Refresh the movies database"""

        if isdir(self.cfg.PATH):
            self.scanDB()
            self.refreshFilesList()
            return(True)

    #---------------------------------------------------------------------#

    def refreshFilesList(self):

        """Refresh the list of files"""

        src = self.ui_srcentry.get()
        # Empty variables :
        self.files = {}
        if self.ui_files.size() > 0:
            self.ui_files.delete(0, END)
        # Get files in DB :
        if src == "" or src == "*":
            if DEBUG:
                print("Get ALL")
            self.loadAllMovies()
        else:
            if DEBUG:
                print("Get '{}'".format(src))
            self.loadSrcMovies(('%'+src+'%',))
        # Sort results :
        liste = list()
        for f, p in self.files.items():
            liste.append(f)
        liste.sort(key=str.lower)
        # Display result :
        for file in liste:
            self.ui_files.insert(END, file)
        return(True)

    #---------------------------------------------------------------------#

    def playUrl1(self):

        """Play URL 1"""

        self.playUrl(self.cfg.URL1)

    def playUrl2(self):

        """Play URL 2"""

        self.playUrl(self.cfg.URL2)

    def playUrl3(self):

        """Play URL 3"""

        self.playUrl(self.cfg.URL3)

    def playUrl4(self):

        """Play URL 4"""

        self.playUrl(self.cfg.URL4)

    def playUrl5(self):

        """Play URL 5"""

        self.playUrl(self.cfg.URL5)

    #---------------------------------------------------------------------#

    def evtPlay(self, evt):
        self.playSelection()

    def evtRefresh(self, evt):
        self.refreshFilesList()

    def evtScan(self, evt):
        self.askToRefreshDataBase()

    def evtCfg(self, cfg):
        self.displayConfig()

    def evtHelp(self, evt):
        self.displayHelp()

    def evtQuit(self, evt):
        self.stop()

    #---------------------------------------------------------------------#

    def createGui(self):

        """Create the GUI for Player"""

        print("*** Creating GUI ***")
        self.root.title("RasPyPlayer v{}".format(VERSION))
        font = Font(self.root, size=20, family='Sans')
        self.root.attributes('-fullscreen', True)

        # Top Frame (search group)
        self.ui_topframe = Frame(self.root, borderwidth=2)
        self.ui_topframe.pack({"side": "top"})
        # Label search
        self.ui_srclabel = Label(self.ui_topframe, text="Search:",
            font=font)
        self.ui_srclabel.grid(row=1, column=0, padx=2, pady=2)
        # Entry search
        self.ui_srcentry = Entry(self.ui_topframe, font=font)
        self.ui_srcentry.grid(row=1, column=1, padx=2, pady=2)
        self.ui_srcentry.bind("<Return>", self.evtRefresh)
        # Button search
        self.ui_srcexec = Button(self.ui_topframe, text="Search",
            command=self.refreshFilesList, font=font)
        self.ui_srcexec.grid(row=1, column=2, padx=2, pady=2)

        # Frame (contain Middle and Url frames)
        self.ui_frame = Frame(self.root, borderwidth=2)
        self.ui_frame.pack(fill=BOTH, expand=1)

        # Middle Frame (files group)
        self.ui_midframe = Frame(self.ui_frame, borderwidth=2)
        self.ui_midframe.pack({"side": "left"}, fill=BOTH, expand=1)
        # Files liste and scrollbar
        self.ui_files = Listbox(self.ui_midframe,
            selectmode=EXTENDED, font=font)
        self.ui_files.pack(side=LEFT, fill=BOTH, expand=1)
        self.ui_files.bind("<Return>", self.evtPlay)
        self.ui_filesscroll = Scrollbar(self.ui_midframe,
            command=self.ui_files.yview)
        self.ui_files.configure(yscrollcommand=self.ui_filesscroll.set)
        self.ui_filesscroll.pack(side=RIGHT, fill=Y)

        # Url Frame (url group)
        self.ui_urlframe = Frame(self.ui_frame, borderwidth=2)
        self.ui_urlframe.pack({"side": "right"})
        # Button Url 1
        self.ui_buturl1 = Button(self.ui_urlframe, textvariable=self.URL1L,
            command=self.playUrl1, font=font)
        self.ui_buturl1.grid(row=1, column=0, padx=2, pady=2)
        # Button Url 2
        self.ui_buturl2 = Button(self.ui_urlframe, textvariable=self.URL2L,
            command=self.playUrl2, font=font)
        self.ui_buturl2.grid(row=2, column=0, padx=2, pady=2)
        # Button Url 3
        self.ui_buturl3 = Button(self.ui_urlframe, textvariable=self.URL3L,
            command=self.playUrl3, font=font)
        self.ui_buturl3.grid(row=3, column=0, padx=2, pady=2)
        # Button Url 4
        self.ui_buturl4 = Button(self.ui_urlframe, textvariable=self.URL4L,
            command=self.playUrl4, font=font)
        self.ui_buturl4.grid(row=4, column=0, padx=2, pady=2)
        # Button Url 5
        self.ui_buturl5 = Button(self.ui_urlframe, textvariable=self.URL5L,
            command=self.playUrl5, font=font)
        self.ui_buturl5.grid(row=5, column=0, padx=2, pady=2)

        # Bottom Frame (buttons group)
        self.ui_botframe = Frame(self.root, borderwidth=2)
        self.ui_botframe.pack({"side": "left"})
        # Button Play
        self.ui_butplay = Button(self.ui_botframe, text="Play",
            command=self.playSelection, font=font)
        self.ui_butplay.grid(row=1, column=0, padx=2, pady=2)
        # Button Refresh
        self.ui_butscan = Button(self.ui_botframe, text="Scan",
            command=self.askToRefreshDataBase, font=font)
        self.ui_butscan.grid(row=1, column=1, padx=2, pady=2)
        # Button Config
        self.ui_butconf = Button(self.ui_botframe, text="Config",
            command=lambda : self.cfg.display(self), font=font)
        self.ui_butconf.grid(row=1, column=2, padx=2, pady=2)
        # Button Help
        self.ui_buthelp = Button(self.ui_botframe, text="Help",
            command=self.displayHelp, font=font)
        self.ui_buthelp.grid(row=1, column=3, padx=2, pady=2)
        # Button Quit
        self.ui_butquit = Button(self.ui_botframe, text="Quit",
            command=self.stop, font=font)
        self.ui_butquit.grid(row=1, column=4, padx=2, pady=2)

        # General bindings
        self.root.bind("<F1>", self.evtHelp)
        self.root.bind("<F2>", self.evtCfg)
        self.root.bind("<F3>", self.evtRefresh)
        self.root.bind("<F5>", self.evtScan)
        self.root.bind("<F12>", self.evtQuit)
        return(True)

    #---------------------------------------------------------------------#

#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
# MAIN PROGRAM
#-------------------------------------------------------------------------#

player = Player()

#-------------------------------------------------------------------------#
# EOF
#-------------------------------------------------------------------------#
