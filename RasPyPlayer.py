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
DEBUG = False

#-------------------------------------------------------------------------#
# MODULES
#-------------------------------------------------------------------------#

from sys import argv
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
# CLASSES
#-------------------------------------------------------------------------#

class Config(object):

    """Configuration class"""

    def __init__(self):
        """Initialisation of the config object"""
        # EXC - Exclude theses directories from movies search
        self.EXC = self.initExcDir()
        # EXC - Exclude theses directories from movies search
        self.EXT = self.initFileExt()
        # DB - Database file name
        self.DB = self.initDbName()
        # OMXSRT - Omxplayer version can handle subtitles
        self.OMXSRT = False
        # OMXCMD - Commands to launch omxplayer
        self.OMXCMD1 = self.initOmxCmd1()
        self.OMXCMD2 = self.initOmxCmd2()
        # DB*** - SQL requests
        self.DBADD = self.initDbAdd()
        self.DBALL = self.initDbAll()
        self.DBSRC = self.initDbSrc()
        self.DBDRP = self.initDbDrp()
        self.DBCRT = self.initDbCrt()

    def initExcDir(self):
        """Initialisation of the excluded directories"""
        res = [
            "Backup", 
            "Musique", 
            "Musique_old", 
            "MacBookPro",
            "Temporary Items", 
            ".TemporaryItems", 
            "MacBook Pro de Julien.sparsebundle",
            "A VOIR"
            ]
        return(res)

    def initFileExt(self):
        """Initialisation of the files extensions"""
        res = [".avi", ".mpg", ".mp4", ".wmv", ".mkv"]
        return(res)

    def initDbName(self):
        """Initialisation of the database name"""
        return("RasPyPlayer.sqlite3")

    def initOmxCmd1(self):
        """Initialisation of the Omx Player command (no subtitles)"""
        res = 'lxterminal --command \"omxplayer \\"{0}\\"\"'
        return(res)

    def initOmxCmd2(self):
        """Initialisation of the Omx Player command (with subtitles)"""
        res = 'lxterminal --command \"omxplayer '
            + '--subtitles \\"{0}\\" \\"{1}\\"\"'
        return(res)

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
        print("*** openDb - opening the database ***")
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
    
    def __init__(self, path):
        """Initialisation of the Player object"""
        self.cfg = None
        self.PATH = path
        self.db = None
        self.files = {}
        self.start()
        self.stop()

    def start(self):
        """Start the Player"""
        print("*** Starting the Player")
        # Configuration
        self.cfg = Config()
        # Database
        self.db = Db(self.cfg)
        if self.db.openDb():
            self.loadAllMovies()
            self.display()
        else:
            error("Database not open")

    def stop(self):
        """Stop the Player"""
        print("*** Stopping the Player")
        self.db.closeDb()
        
    def scanDB(self):
        """Add movies in DB"""
        print("*** Adding movies in database")
        scanFiles(self.db, self.cfg, self.path)
        self.db.commitDb()

    def loadAllMovies(self):
        """Load movies from DB"""
        self.files = self.db.getAllMovies()

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

    def display(self):
        """Display the player"""
        self.createGui()
        #self.root.mainloop()

    def createGui(self):
        """Create the GUI for Player"""
        print("*** Creating GUI ***")

#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
# MAIN PROGRAM
#-------------------------------------------------------------------------#

if len(argv) == 2:
    print("{}".format(argv[0]))
    print("Path: {}".format(argv[1]))
    player = Player(argv[1])
else:
    print("Usage: {} /path/to/medias".format(argv[0]))

#-------------------------------------------------------------------------#
# EOF
#-------------------------------------------------------------------------#
