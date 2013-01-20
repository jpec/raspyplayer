#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# RasPyPlayer.py - Movies player for Raspberry Pi
#-------------------------------------------------------------------------#
VERSION = "2.0-dev"
#-------------------------------------------------------------------------#
# Author :Julien Pecqueur (JPEC)
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

# DB - Database file
DB = "RasPyPlayer.sqlite3"

# OMXCMD - Commands to launch omxplayer :
OMXCMD1 = 'lxterminal --command \"omxplayer \\"{0}\\"\"'
OMXCMD2 = 'lxterminal --command \"omxplayer --subtitles \\"{0}\\" \\"{1}\\"\"'

# OMXSRT - Omxplayer version can handle subtitles (False / True) :
OMXSRT = False

# EXT - Movies extensions to add in movie database :
EXT = [".avi", ".mpg", ".mp4", ".wmv", ".mkv"]

# EXC - Exclude theses directories from movies search :
EXC = ["Backup",
       "Musique",
       "Musique_old",
       "MacBookPro",
       "Temporary Items",
       ".TemporaryItems",
       "MacBook Pro de Julien.sparsebundle",
       "A VOIR"]


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

def scanFiles(db, path):
    
    """Look for movies in path to add in DB."""
    
    if DEBUG:
        print("Scan {0}".format(path))
    for file in os.listdir(path):
        filepath = path+"/"+file
        if len(file) > 4 and file[-4: len(file)] in EXT \
            and file[0:1] != ".":
            # File
            db.addMovie(os.path.basename(file), filepath)
        elif os.path.isdir(filepath) and not file in EXC \
            and file[0:1] != ".":
            # Directory
            scanFiles(db, filepath)

#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
# CLASSES
#-------------------------------------------------------------------------#

class Db(object):
    
    """DataBase class"""
    
    def __init__(self, db):
        """Initialisation of the DB object"""
        self.db = db
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
        print("*** createDb - Creating the database ***")
        self.execSql("CREATE TABLE files (file, path)", False)
        self.commitDb()
        return(True)

    def dropDb(self):
        "Drop the DB"
        print("*** dropDb - Drop the database ***")
        self.execSql("DROP TABLE files", False)
        return(True)

    def initDb(self):
        """Initialisation of the DB"""
        print("*** initDb - Initializing the database ***")
        self.dropDb()
        self.createDb()
        return(True)

    def closeDb(self):
        """Close the DB"""
        print("*** closeDb - Closing the database ***")
        self.cur.close()
        self.con.close()
        self.cur = None
        self.con = None
        return(True)

    def commitDb(self):
        """Commit"""
        print("*** commitDb - Commiting the database ***")
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
        print("*** getAllMovies - Getting all movies from database ***")
        files = {}
        self.execSql("SELECT * FROM files ORDER BY file", False)
        for file, path in self.cur:
            files[file] = path
        return(files)
    
    def getSrcMovies(self, src):
        """Return movies from DB with search pattern"""
        print("*** getSrcMovies - Searching movies in database ***")
        files = {}
        self.execSql("SELECT * FROM files WHERE file LIKE ? ORDER BY file", src)
        for file, path in self.cur:
            files[file] = path
        return(files)

    def addMovie(self, file, filepath):
        """Add a movie in DB"""
        self.execSql("INSERT INTO files VALUES (?, ?)", (file, filepath))
        return(True)

#-------------------------------------------------------------------------#

class Player(object):

    """Player class"""
    
    def __init__(self, db, path):
        """Initialisation of the Player object"""
        self.DB = db
        self.PATH = path
        self.db = None
        self.files = {}
        self.start()
        self.display()
        self.stop()



    def start(self):
        """Start the Player"""
        print("*** Starting the Player")
        self.db = Db(self.DB)
        if self.db.openDb():
            self.loadAllMovies()

			
    def stop(self):
        """Stop the Player"""
        self.db.closeDb()
        print("*** Stoping the Player")

    def scanDB(self):
        """Add movies in DB"""
        print("*** Adding movies in database")
        scanFiles(self.db, self.path)
        self.db.commitDb()

    def loadAllMovies(self):
        """Load movies from DB"""
        self.files = self.db.getAllMovies()

    def play(self, file):
        """Play a movie"""
        print("Playing {}".format(file))
        sub = file[0:-3] + "srt"
        if OMXSRT and os.path.isfile(sub):
            cmd = OMXCMD2.format(sub, file)
        else:
            cmd = OMXCMD1.format(file)
        print(cmd)
        os.system(cmd)

    def display(self):
        """Display the player"""
        
        #self.root.mainloop()

#-------------------------------------------------------------------------#

#-------------------------------------------------------------------------#
# MAIN PROGRAM
#-------------------------------------------------------------------------#

if len(argv) == 2:
    print("{}".format(argv[0]))
    print("Database: {}".format(DB))
    print("Path:     {}".format(argv[1]))
    player = Player(DB, argv[1])
else:
    print("Usage: {} /path/to/medias".format(argv[0]))


#---------/---------------------------------------------------------------#
# EOF
#-------------------------------------------------------------------------#
