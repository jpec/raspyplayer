#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# RasPyPlayer.py - Movies player for Raspberry Pi
#-------------------------------------------------------------------------#
VERSION = "2.0-dev"
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
DEBUG = True

#-------------------------------------------------------------------------#
# MODULES
#-------------------------------------------------------------------------#

import os
import sqlite3
import tkinter
import tkinter.messagebox
import tkinter.font

#-------------------------------------------------------------------------#
# FUNCTIONS
#-------------------------------------------------------------------------#

def scanFiles(db, cfg, path):
    
    """Look for movies in path to add in DB."""
    
    if DEBUG:
        print("Scan {0}".format(path))
    for file in os.listdir(path):
        filepath = path+"/"+file
        if len(file) > 4 and file[-4: len(file)] in cfg.EXT \
            and file[0:1] != ".":
            # File
            db.addMovie(os.path.basename(file), filepath)
        elif os.path.isdir(filepath) and not file in cfg.EXC \
            and file[0:1] != ".":
            # Directory
            scanFiles(db, cfg, filepath)

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

    Keyboard shortcuts in RasPyPlayer :
    F1 : Help
    F3 : Search
    F4 : Play
    F5 : Refresh

    Keyboard shortcuts during playback :
    n : Previous subtitle
    m : Next subtitle
    s : Toggle subtitle
    q : Quit playback
    p : Pause/Resume (space)
    - : Lower volume
    + : Higher volume
    Left : Seek -30
    Right : Seek +30
    Down : Seek -600
    Up : Seek +600
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
        self.OMXSRT = None
        # Values hard coded
        self.OMXCMD1='lxterminal --command \"omxplayer \\"{0}\\"\"'
        self.OMXCMD2='lxterminal --command \"omxplayer --subtitles \\"{0}\\" \\"{1}\\"\"'
        # DB*** - SQL requests
        self.DBADD = self.initDbAdd()
        self.DBALL = self.initDbAll()
        self.DBSRC = self.initDbSrc()
        self.DBDRP = self.initDbDrp()
        self.DBCRT = self.initDbCrt()

    def readConf(self):
        """Read the CONF file"""
        if os.path.isfile(self.CONF):
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
                elif len(l) >= 7 and l[0:7] == "OMXSRT=":
                    self.OMXSRT = l[7:len(l)]
                    if DEBUG:
                        print(l)
            f.close()
            return(True)
        else:
            return(False)

    def initDbAdd(self):
        """Initialisation of the DBADD request"""
        res = "INSERT INTO files VALUES (?, ?)"
        return(res)

    def initDbSrc(self):
        """Initialisation of the DBSRC request"""
        res = "SELECT * FROM files WHERE file LIKE ? ORDER BY file"
        return(res)

    def initDbAll(self):
        """Initialisation of the DBALL request"""
        res = "SELECT * FROM files ORDER BY file"
        return(res)

    def initDbDrp(self):
        """Initialisation of the DBDRP request"""
        res = "DROP TABLE files"
        return(res)

    def initDbCrt(self):
        """Initialisation of the DBCRT request"""
        res = "CREATE TABLE files (file, path)"
        return(res)

    def display(self, root):
        """Display the setting window"""
        # TODO

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

    def openDb(self):
        """Open the DB"""
        print("*** DB - Opening the database ***")
        new = False
        if not os.path.isfile(self.db):
            new = True
        self.con = sqlite3.connect(self.db)
        self.cur = self.con.cursor()
        if new:
            self.createDb()
        return(True)

    def createDb(self):
        """Create the DB"""
        print("*** DB - Creating the database ***")
        self.execSql(self.cfg.DBCRT, False)
        self.commitDb()
        return(True)

    def dropDb(self):
        "Drop the DB"
        print("*** DB - Dropping the database ***")
        self.execSql(self.cfg.DBDRP, False)
        return(True)

    def initDb(self):
        """Initialisation of the DB"""
        print("*** DB - Initializing the database ***")
        self.dropDb()
        self.createDb()
        return(True)

    def closeDb(self):
        """Close the DB"""
        print("*** DB - Closing the database ***")
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None
        return(True)

    def commitDb(self):
        """Commit"""
        print("*** DB - Commiting the database ***")
        self.con.commit()
        
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

    def getAllMovies(self):
        """Return all movies from DB"""
        files = {}
        self.execSql(self.cfg.DBALL, False)
        for file, path in self.cur:
            files[file] = path
        return(files)
    
    def getSrcMovies(self, src):
        """Return movies from DB with search pattern"""
        files = {}
        self.execSql(self.cfg.DBSRC, src)
        for file, path in self.cur:
            files[file] = path
        return(files)

    def addMovie(self, file, filepath):
        """Add a movie in DB"""
        self.execSql(self.cfg.DBADD, (file, filepath))
        return(True)

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

    def start(self):
        """Start the Player"""
        print("*** Starting the Player ***")
        # Configuration
        self.cfg = Config()
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

    def stop(self):
        """Stop the Player"""
        print("*** Stopping the Player ***")
        self.db.closeDb()
        self.root.destroy()
        
    def scanDB(self):
        """Add movies in DB"""
        print("*** Adding movies in database")
        scanFiles(self.db, self.cfg, self.cfg.PATH)
        self.db.commitDb()
        return(True)

    def loadAllMovies(self):
        """Load movies from DB"""
        self.files = self.db.getAllMovies()
        return(True)

    def loadSrcMovies(self, src):
        """Load movies matching search pattern"""
        self.files = self.db.getSrcMovies(src)
        return(True)

    def play(self, file):
        """Play a movie"""
        print("Playing {}".format(file))
        sub = file[0:-3] + "srt"
        if self.cfg.OMXSRT and os.path.isfile(sub):
            cmd = self.cfg.OMXCMD2.format(sub, file)
        else:
            cmd = self.cfg.OMXCMD1.format(file)
        if DEBUG:
            print(cmd)
        os.system(cmd)
        return(True)

    def displayHelp(self):
        """Display help"""
        tkinter.messagebox.showinfo("Help...", getHelp())
        return(True)

    def playSelection(self):
        """Play selected files"""
        sel = self.ui_files.curselection()
        for i in sel:
            f = self.ui_files.get(i)
            self.play(self.files[f])
        return(True)

    def display(self):
        """Display the player"""
        self.createGui()
        self.refreshDataBase()
        self.root.mainloop()

    def askToRefreshDataBase(self):
        """Ask to refresh database"""
        msg = "Do you want to refresh the movies database ?"
        res = tkinter.messagebox.askokcancel("RasPyPlayer", msg)
        if res:
            self.refreshDataBase()
        return(True)

    def refreshDataBase(self):
        """Refresh the movies database"""
        scanFiles(self.db, self.cfg, self.cfg.PATH)
        self.refreshFilesList()
        return(True)

    def refreshFilesList(self):
        """Refresh the list of files"""
        src = self.ui_srcentry.get()
        # Empty variables :
        self.files = {}
        if self.ui_files.size() > 0:
            self.ui_files.delete(0, tkinter.END)
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
            self.ui_files.insert(tkinter.END, file)
        return(True)

    def createGui(self):
        """Create the GUI for Player"""
        print("*** Creating GUI ***")
        self.root = tkinter.Tk()
        self.root.title("RasPyPlayer v{}".format(VERSION))
        font = tkinter.font.Font(self.root, size=20, family='Sans')
        self.root.attributes('-fullscreen', True)
        self.root.attributes('-topmost', True)
        # Top Frame (search group)
        self.ui_topframe = tkinter.Frame(self.root, borderwidth=2)
        self.ui_topframe.pack({"side": "top"})
        # Label search
        self.ui_srclabel = tkinter.Label(self.ui_topframe,
                                     text="Search:",
                                     font=font
                                     )
        self.ui_srclabel.grid(row=1, column=0, padx=2, pady=2)
        # Entry search
        self.ui_srcentry = tkinter.Entry(self.ui_topframe, font=font)
        self.ui_srcentry.grid(row=1, column=1, padx=2, pady=2)
        # Button search
        self.ui_srcexec = tkinter.Button(self.ui_topframe,
                                     text="Search",
                                     command=self.refreshFilesList,
                                     font=font
                                     )
        self.ui_srcexec.grid(row=1, column=2, padx=2, pady=2)
        # Middle Frame (files group)
        self.ui_midframe = tkinter.Frame(self.root, borderwidth=2)
        self.ui_midframe.pack(fill=tkinter.BOTH, expand=1)
        # Files liste and scrollbar
        self.ui_files = tkinter.Listbox(self.ui_midframe,
                                       selectmode=tkinter.EXTENDED,
                                       font=font
                                       )
        self.ui_files.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.ui_filesscroll = tkinter.Scrollbar(self.ui_midframe,
                                          command=self.ui_files.yview
                                          )
        self.ui_files.configure(yscrollcommand=self.ui_filesscroll.set)
        self.ui_filesscroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # Bottom Frame (buttons group)
        self.ui_botframe = tkinter.Frame(self.root, borderwidth=2)
        self.ui_botframe.pack({"side": "left"})
        # Button Play
        self.ui_butplay = tkinter.Button(self.ui_botframe,
                                     text="Play",
                                     command=self.playSelection,
                                     font=font
                                     )
        self.ui_butplay.grid(row=1, column=0, padx=2, pady=2) 
        # Button Refresh
        self.ui_butscan = tkinter.Button(self.ui_botframe,
                                     text="Scan",
                                     command=self.askToRefreshDataBase,
                                     font=font
                                     )
        self.ui_butscan.grid(row=1, column=1, padx=2, pady=2)       
        # Button Help
        self.ui_buthelp = tkinter.Button(self.ui_botframe,
                                     text="Help",
                                     command=self.displayHelp,
                                     font=font
                                     )
        self.ui_buthelp.grid(row=1, column=2, padx=2, pady=2)
        # Button Quit
        self.ui_butquit = tkinter.Button(self.ui_botframe,
                                     text="Quit",
                                     command=self.stop,
                                     font=font
                                     )
        self.ui_butquit.grid(row=1, column=3, padx=2, pady=2)
        return(True)

#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
# MAIN PROGRAM
#-------------------------------------------------------------------------#

player = Player()

#-------------------------------------------------------------------------#
# EOF
#-------------------------------------------------------------------------#
