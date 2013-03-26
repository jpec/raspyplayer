#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# RasPyPlayer.py - Movies player originally designed for Raspberry Pi.
#-------------------------------------------------------------------------#
VERSION = "2.1.0"
#-------------------------------------------------------------------------#
# Author :  Julien Pecqueur (JPEC)
# Email :   jpec@julienpecqueur.net
# Site :    http://raspyplayer.org
# Sources : https://github.com/jpec/RasPyPlayer
# Bugs :    https://github.com/jpec/RasPyPlayer/issues
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
from sqlite3 import connect
from tkinter import Tk
from tkinter import Frame
from tkinter import Label
from tkinter import Entry
from tkinter import Button
from tkinter import Listbox
from tkinter import Scrollbar
from tkinter import EXTENDED
from tkinter import BOTH
from tkinter import W
from tkinter import Y
from tkinter import LEFT
from tkinter import RIGHT
from tkinter import END
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
        if len(file) > 4 and file[-4: len(file)] in cfg.EXT \
            and file[0:1] != ".":
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
    msg = """
    RasPyPlayer, v{0}
    Author : Julien Pecqueur (JPEC)
    Email : jpec@julienpecqueur.net
    Home : http://raspyplayer.org
    Sources : https://github.com/jpec/RasPyPlayer
    Bugs : https://github.com/jpec/RasPyPlayer/issues
    License : GPL
    """
    return(msg.format(VERSION))

#-------------------------------------------------------------------------#
# CLASSES
#-------------------------------------------------------------------------#

class Config(object):

    """Configuration class"""

    def __init__(self):

        """Initialisation of the config object"""

        self.CONF = "/etc/raspyplayer.conf"
        # Values loaded from CONF file
        self.PATH = None
        self.EXC = []
        self.EXT = []
        self.DB = None
        # Values hard coded
        self.MPLRCMD = 'xterm -e mplayer -fs \"{0}\"'
        self.OMXCMD1 = 'xterm -e omxplayer \"{0}\"'
        self.OMXCMD2 = 'xterm -e omxplayer --subtitles \"{0}\" \"{1}\"'
        # DB*** - SQL requests
        self.DBADD = self.initDbAdd()
        self.DBALL = self.initDbAll()
        self.DBSRC = self.initDbSrc()
        self.DBDRP = self.initDbDrp()
        self.DBCRT = self.initDbCrt()

    #---------------------------------------------------------------------#

    def clearConf(self):

        """Clear conf settinfs"""

        self.PATH = None
        self.EXC = []
        self.EXT = []
        self.DB = None

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

    #---------------------------------------------------------------------#

    def reload(self):

        """Load the conf from the setting window"""

        self.PATH = self.ui_path.get()
        self.EXC = str2lst(self.ui_exc.get())
        self.EXT = str2lst(self.ui_ext.get())
        self.DB = self.ui_db.get()

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
        f.close()
        if self.checkConf():
            self.root.destroy()

    #---------------------------------------------------------------------#

    def createGui(self):

        """Create the GUI for Config"""

        print("*** Creating Configuration GUI ***")
        self.root = Tk()
        self.root.title("Configuration")
        self.root.attributes('-topmost', True)
        font = Font(self.root, size=20, family='Sans')
        # Middle Frame (config group)
        self.ui_midframe = Frame(self.root, borderwidth=2)
        self.ui_midframe.pack(fill=BOTH, expand=1)
        # PATH
        self.ui_pathlbl = Label(self.ui_midframe,
                                text="Movies root folder",
                                justify=LEFT,
                                anchor=W,
                                font=font
                                )
        self.ui_pathlbl.grid(row=1, column=0, padx=2, pady=2)
        self.ui_path = Entry(self.ui_midframe, font=font)
        self.ui_path.grid(row=1, column=1, padx=2, pady=2)
        # EXC
        self.ui_exclbl = Label(self.ui_midframe,
                               text="Directories to exclude",
                               justify=LEFT,
                               anchor=W,
                               font=font
                               )
        self.ui_exclbl.grid(row=2, column=0, padx=2, pady=2)
        self.ui_exc = Entry(self.ui_midframe, font=font)
        self.ui_exc.grid(row=2, column=1, padx=2, pady=2)
        # EXT
        self.ui_extlbl = Label(self.ui_midframe,
                               text="Movies extensions",
                               justify=LEFT,
                               anchor=W,
                               font=font
                               )
        self.ui_extlbl.grid(row=3, column=0, padx=2, pady=2)
        self.ui_ext = Entry(self.ui_midframe, font=font)
        self.ui_ext.grid(row=3, column=1, padx=2, pady=2)
        # DB
        self.ui_dblbl = Label(self.ui_midframe,
                              text="Database name",
                              justify=LEFT,
                              anchor=W,
                              font=font
                              )
        self.ui_dblbl.grid(row=4, column=0, padx=2, pady=2)
        self.ui_db = Entry(self.ui_midframe, font=font)
        self.ui_db.grid(row=4, column=1, padx=2, pady=2)
        # Bottom Frame (buttons group)
        self.ui_botframe = Frame(self.root, borderwidth=2)
        self.ui_botframe.pack({"side": "left"})
        # Button Save
        self.ui_butsave = Button(self.ui_botframe,
                                 text="Save",
                                 command=self.save,
                                 font=font
                                 )
        self.ui_butsave.grid(row=1, column=0, padx=2, pady=2)
        # Button Close
        self.ui_butquit = Button(self.ui_botframe,
                                 text="Close",
                                 command=self.root.destroy,
                                 font=font
                                 )
        self.ui_butquit.grid(row=1, column=1, padx=2, pady=2)
        return(True)
    #---------------------------------------------------------------------#

#-------------------------------------------------------------------------#

class Db(object):

    """DataBase class"""

    def __init__(self, cfg):

        """Initialisation of the DB object"""

        self.cfg = cfg
        self.db = cfg.DB
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

        "Drop the DB"

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
        self.root = None
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
        if self.cfg.readConf():
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

        print("*** Stopping the Player ***")
        self.db.closeDb()
        self.root.destroy()

    #---------------------------------------------------------------------#

    def scanDB(self):

        """Add movies in DB"""

        print("*** Adding movies in database")
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

    def play(self, file):

        """Play a movie"""

        print("Playing {}".format(file))
        if self.cfg.useOmx():
            sub = file[0:-3] + "srt"
            if isfile(sub):
                cmd = self.cfg.OMXCMD2.format(sub, file)
            else:
                cmd = self.cfg.OMXCMD1.format(file)
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

        self.cfg.display(self.root)
        return(True)

    #---------------------------------------------------------------------#

    def playSelection(self):

        """Play selected files"""

        sel = self.ui_files.curselection()
        for i in sel:
            f = self.ui_files.get(i)
            self.play(self.files[f])
        return(True)

    #---------------------------------------------------------------------#

    def display(self):

        """Display the player"""

        self.createGui()
        self.refreshDataBase()
        self.root.mainloop()

    #---------------------------------------------------------------------#

    def askToRefreshDataBase(self):

        """Ask to refresh database"""

        msg = "Do you want to refresh the movies database ?"
        res = messagebox.askokcancel("RasPyPlayer", msg)
        if res:
            self.refreshDataBase()
        return(True)

    #---------------------------------------------------------------------#

    def refreshDataBase(self):

        """Refresh the movies database"""

        if isdir(self.cfg.PATH):
            scanFiles(self.db, self.cfg, self.cfg.PATH)
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

    def createGui(self):

        """Create the GUI for Player"""

        print("*** Creating GUI ***")
        self.root = Tk()
        self.root.title("RasPyPlayer v{}".format(VERSION))
        font = Font(self.root, size=20, family='Sans')
        self.root.attributes('-fullscreen', True)
        #self.root.attributes('-topmost', True)
        # Top Frame (search group)
        self.ui_topframe = Frame(self.root, borderwidth=2)
        self.ui_topframe.pack({"side": "top"})
        # Label search
        self.ui_srclabel = Label(self.ui_topframe,
                                 text="Search:",
                                 font=font
                                 )
        self.ui_srclabel.grid(row=1, column=0, padx=2, pady=2)
        # Entry search
        self.ui_srcentry = Entry(self.ui_topframe, font=font)
        self.ui_srcentry.grid(row=1, column=1, padx=2, pady=2)
        # Button search
        self.ui_srcexec = Button(self.ui_topframe,
                                 text="Search",
                                 command=self.refreshFilesList,
                                 font=font
                                 )
        self.ui_srcexec.grid(row=1, column=2, padx=2, pady=2)
        # Middle Frame (files group)
        self.ui_midframe = Frame(self.root, borderwidth=2)
        self.ui_midframe.pack(fill=BOTH, expand=1)
        # Files liste and scrollbar
        self.ui_files = Listbox(self.ui_midframe,
                                selectmode=EXTENDED,
                                font=font
                                )
        self.ui_files.pack(side=LEFT, fill=BOTH, expand=1)
        self.ui_filesscroll = Scrollbar(self.ui_midframe,
                                        command=self.ui_files.yview
                                        )
        self.ui_files.configure(yscrollcommand=self.ui_filesscroll.set)
        self.ui_filesscroll.pack(side=RIGHT, fill=Y)
        # Bottom Frame (buttons group)
        self.ui_botframe = Frame(self.root, borderwidth=2)
        self.ui_botframe.pack({"side": "left"})
        # Button Play
        self.ui_butplay = Button(self.ui_botframe,
                                 text="Play",
                                 command=self.playSelection,
                                 font=font
                                 )
        self.ui_butplay.grid(row=1, column=0, padx=2, pady=2)
        # Button Refresh
        self.ui_butscan = Button(self.ui_botframe,
                                 text="Scan",
                                 command=self.askToRefreshDataBase,
                                 font=font
                                 )
        self.ui_butscan.grid(row=1, column=1, padx=2, pady=2)
        # Button Config
        self.ui_butconf = Button(self.ui_botframe,
                                 text="Config",
                                 command=self.displayConfig,
                                 font=font
                                 )
        self.ui_butconf.grid(row=1, column=2, padx=2, pady=2)
        # Button Help
        self.ui_buthelp = Button(self.ui_botframe,
                                 text="Help",
                                 command=self.displayHelp,
                                 font=font
                                 )
        self.ui_buthelp.grid(row=1, column=3, padx=2, pady=2)
        # Button Quit
        self.ui_butquit = Button(self.ui_botframe,
                                 text="Quit",
                                 command=self.stop,
                                 font=font
                                 )
        self.ui_butquit.grid(row=1, column=4, padx=2, pady=2)
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
