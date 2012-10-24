#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------#
# RasPyPlayer.py - Movies player for Raspberry Pi
#-------------------------------------------------------------------------#
VERSION = "0.1-dev"
#-------------------------------------------------------------------------#
# Auteur : Julien Pecqueur (JPEC)
# Email : jpec@julienpecqueur.net
# Site : http://julienpecqueur.net
# Sources : https://github.com/jpec/RasPyPlayer
# Bugs : https://github.com/jpec/RasPyPlayer/issues
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
# IMPORTATION DES MODULES                                                 #
#-------------------------------------------------------------------------#
import os
import tkinter
import tkinter.messagebox
import sqlite3

#-------------------------------------------------------------------------#
# PARAMETRAGE PROGRAMME                                                   #
#-------------------------------------------------------------------------#
# PATH - Chemin vers le dossier racine contenant les vidéos :
PATH = "/home/pi/nas"

# OMXCMD - Commande pour lancer le player omxplayer :
OMXCMD = "lxterminal --command \"omxplayer -o hdmi '{0}'\""

# EXT - Extensions des fichiers vidéos à ajouter dans la librairie :
EXT = [".avi", ".mpg", ".mp4", ".wmv"]

# EXC - Répertoires à exclure de la recherche des vidéos :
EXC = ["Backup",
       "Musique",
       "MacBookPro",
       "Temporary Items",
       "MacBook Pro de Julien.sparsebundle",
       "A VOIR"]

# DB - Nom base de données locale :
DB = "RasPyPlayer.sqlite3"

# DBCREATE - Requête SQL pour créer la table "files" :
DBCREATE = "CREATE TABLE files (file, path)"

# DBADD - Requête SQL pour ajouter une ligne dans "files" :
DBADD = "INSERT INTO files VALUES (?, ?)"

# DBDROP - Requête SQL pour droper la table "files" :
DBDROP = "DROP TABLE files"

# DBALL - Requête SQL pour lister toutes les lignes de "files" :
DBALL = "SELECT * FROM files ORDER BY file"

# DBSRC - Requête SQL pour rechercher des lignes dans "files" :
DBSRC = "SELECT * FROM files WHERE file LIKE ? ORDER BY file"

# DEBUG - Mode debug (0 - off / 1 - on) :
DEBUG = 0

#-------------------------------------------------------------------------#
# CHAINES                                                                 #
#-------------------------------------------------------------------------#
M_TITLE = "RasPyPlayer"
M_INIT = "Initialisation de la base de données"
M_SCAN = "Scanning : {0}"
M_LIST = "Listing :"
M_BTSCAN = "Scanner"
M_BTPLAY = "Lecture"
M_BTHELP = "Aide"
M_BTQUIT = "Quitter"
M_BTSEARCH = "Go"
M_SEARCH = "Recherche :"

#-------------------------------------------------------------------------#
# DEFINITION DES CLASSES                                                  #
#-------------------------------------------------------------------------#
class Player(object):
    def __init__(self, path, db):
        """Constructeur de la classe Player"""
        self.path = path
        self.db = db
        self.files = {}
        self.conDB = False
        self.curDB = False
        self.topDB = False
        self.search = False
        self.creerGui()
        self.openDB()
        self.listFiles()
        self.displayFiles()

    def openDB(self):
        """Ouvre la base de donnée, la créé le cas échéant"""
        sql = False
        bind = False
        if os.path.isfile(self.db):
            self.topDB = True
        self.conDB = sqlite3.connect(self.db)
        self.curDB = self.conDB.cursor()

    def initDB(self):
        """Initialisation de la base de données"""
        if DEBUG:
            print(M_INIT)
        if self.topDB:
            self.execDB(DBDROP, False)
        self.execDB(DBCREATE, False)
        self.topDB = True

    def closeDB(self):
        """Ferme la base de données"""
        self.curDB.close()
        self.conDB.close()

    def execDB(self, sql, bind):
        """Exécute une requête dans la base de données"""
        if sql:
            if bind:
                if DEBUG:
                    print(sql, bind)
                self.curDB.execute(sql, bind)
            else:
                self.curDB.execute(sql)
            self.conDB.commit() 

    def refreshBase(self):
        """Rafraîchi la base de données"""
        if not self.topDB:
            self.initDB()
        self.scanFiles(self.path)
        self.listFiles()

    def scanFiles(self, path):
        """Scan les répertoires et alimente la base de données"""
        if DEBUG:
            print(M_SCAN.format(path))
        for file in os.listdir(path):
            filepath = path+"/"+file
            if len(file) > 4 and file[-4: len(file)] in EXT \
               and file[0:1] != ".":
                # Si c'est un fichier vidéo alors on l'ajoute
                self.execDB(DBADD, (os.path.basename(file), filepath))
            elif os.path.isdir(filepath) and not file in EXC:
                # Si c'est un répertoire et qu'il n'est pas
                # dans les exclusions alors on le scanne
                self.scanFiles(filepath)
    
    def searchFiles(self):
        """Recherche les fichiers"""
        s = self.w_search.get()
        if s:
            self.search = ('%'+s+'%',)
        else:
            self.search = False
        self.initFiles()
        self.listFiles()
        self.displayFiles()

    def listFiles(self):
        """Liste les fichiers présents dans la base"""
        if not self.topDB:
            self.initDB()
        if DEBUG:
            print(M_LIST)
        if self.search:
            self.execDB(DBSRC, self.search)
        else:
            self.execDB(DBALL, False)
        for file, path in self.curDB:
            if DEBUG:
                print(file, path)
            self.files[file] = path

    def playFile(self, file):
        """Joue le fichier passé en paramètre"""
        if DEBUG:
            print(OMXCMD.format(file))
        os.system(OMXCMD.format(file))

    def displayFiles(self):
        """Affiche la liste des fichiers"""
        liste = list()
        for f, p in self.files.items():
            liste.append(f)
        liste.sort(key=str.lower)
        for file in liste:
            if DEBUG:
                print(file)
            self.w_files.insert(tkinter.END, file)

    def initFiles(self):
        """Initialise les listes de fichiers"""
        self.files = {}
        if self.w_files.size() > 0:
            self.w_files.delete(0, tkinter.END)
            
    def refreshFiles(self):
        """Rafraichit la liste des fichiers"""
        self.initFiles()
        self.refreshBase()
        self.displayFiles()
        
    def playSelection(self):
        """Lire le fichier sélectionné"""
        sel = self.w_files.curselection()
        for i in sel:
            f = self.w_files.get(i)
            self.playFile(self.files[f])
        
    def creerGui(self):
        """Construction de la fenêtre"""
        self.root = tkinter.Tk()
        self.root.title(M_TITLE)
        # Centrage fenêtre
        w = 800
        h = 600
        ws = self.root.winfo_screenwidth()
        hs = self.root.winfo_screenheight()
        x = (ws/2) - (w/2)
        y = (hs/2) - (h/2)
        self.root.geometry('%dx%d+%d+%d' % (w, h, x, y))
	# Zone recherche
        self.topframe = tkinter.Frame(self.root, borderwidth=2)
        self.topframe.pack({"side": "top"})
        # Input recherche
        self.w_label = tkinter.Label(self.topframe, text=M_SEARCH)
        self.w_label.grid(row=1, column=0, padx=2, pady=2)
        self.w_search = tkinter.Entry(self.topframe)
        self.w_search.grid(row=1, column=1, padx=2, pady=2)
        # Bouton rechercher
        self.w_exec = tkinter.Button(self.topframe,
                                     text=M_BTSEARCH,
                                     command=self.searchFiles
                                     )
        self.w_exec.grid(row=1, column=2, padx=2, pady=2)
        # Zone liste fichiers
        self.midframe = tkinter.Frame(self.root, borderwidth=2)
        self.midframe.pack(fill=tkinter.BOTH, expand=1)
        # Liste des fichiers
        self.w_files = tkinter.Listbox(self.midframe)
        self.w_files.pack(side=tkinter.LEFT, fill=tkinter.BOTH, expand=1)
        self.w_scroll = tkinter.Scrollbar(self.midframe,
                                          command=self.w_files.yview)
        self.w_files.configure(yscrollcommand=self.w_scroll.set)
        self.w_scroll.pack(side=tkinter.RIGHT, fill=tkinter.Y)
        # Groupe boutons
        self.botframe = tkinter.Frame(self.root, borderwidth=2)
        self.botframe.pack({"side": "left"})
        # Bouton Play
        self.w_play = tkinter.Button(self.botframe,
                                     text=M_BTPLAY,
                                     command=self.playSelection,
                                     fg='green'
                                     )
        self.w_play.grid(row=1, column=0, padx=2, pady=2) 
        # Bouton Refresh
        self.w_scan = tkinter.Button(self.botframe,
                                     text=M_BTSCAN,
                                     command=self.refreshFiles,
                                     fg='red'
                                     )
        self.w_scan.grid(row=1, column=1, padx=2, pady=2)       
        # Bouton Help
        self.w_help = tkinter.Button(self.botframe,
                                     text=M_BTHELP,
                                     command=self.displayHelp
                                     )
        self.w_help.grid(row=1, column=2, padx=2, pady=2)
        # Bouton Quit
        self.w_quit = tkinter.Button(self.botframe,
                                     text=M_BTQUIT,
                                     command=self.closePlayer
                                     )
        self.w_quit.grid(row=1, column=3, padx=2, pady=2)
        
    def displayHelp(self):
        """Affiche l'aide"""
        msg = "RasPyPlayer, v{0}\n"
        msg += "Auteur : Julien Pecqueur (JPEC)\n"
        msg += "Email : jpec@julienpecqueur.net\n"
        msg += "Site : http://julienpecqueur.net\n"
        msg += "Sources : https://github.com/jpec/RasPyPlayer\n"
        msg += "Bugs : https://github.com/jpec/RasPyPlayer/issues\n"
        msg += "License : GNUGPL\n"
        msg += "\n"
        msg += "Raccourcis clavier pendant la lecture :\n"
        msg += "n : Sous-titre précédent\n"
        msg += "m : Sous-titre suivant\n"
        msg += "s : Bascule de sous-titre\n"
        msg += "q : Quitte le lecteur\n"
        msg += "p : Pause/Reprise (espace)\n"
        msg += "- : Baisse le volume\n"
        msg += "+ : Monte le volume\n"
        msg += "Left : Seek -30\n"
        msg += "Right : Seek +30\n"
        msg += "Down : Seek -600\n"
        msg += "Up : Seek +600\n"
        tkinter.messagebox.showinfo("Aide", msg.format(VERSION))
        
    def closePlayer(self):
        """Quitte l'application"""
        self.closeDB()
        self.root.destroy()
        
#-------------------------------------------------------------------------#
# PROGRAMME PRINCIPAL                                                     #
#-------------------------------------------------------------------------#

player = Player(PATH, DB)
player.root.mainloop()

#-------------------------------------------------------------------------#
# EOF                                                                     #
#-------------------------------------------------------------------------#
