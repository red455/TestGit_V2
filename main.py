import os
from tkinter import *

import datetime
import re
import subprocess

root = Tk()
# Défini l'année en cours
currentDateTime = datetime.datetime.now()
date = currentDateTime.date()
year = date.strftime("%y")

# on indique le chemin de explorer.exe
FILEBROWSER_PATH = os.path.join(os.getenv('WINDIR'), 'explorer.exe')

        


def retrieve_input():
    global year
    # je vais scruter dans dossier_principal
    # ~ correspond au home user
    dossier_principal = (os.path.expanduser("~/Arcalu Dropbox/A CLASSER/TEST")).replace("\\", "/")
    # interroger utilisateur et récupérer le contenu dans inputValue
    inputValue = textBox.get("1.0", "end-1c")
    # pour tout ce qui traine sous path_source, on récupère 3 variables
    #  root : le chemin sauf le nom du fichier
    #  d_names : les dossiers
    #  f_names : les fichiers
    for root, d_names, f_names in os.walk(dossier_principal, topdown=True):
        # dans le dossier en cours, on récupère l'ensemble des dossiers
        # chaque fichier en cours va être accessible via filename
        for dossier in d_names:
            # dossier_full_path contient le chemin complet qui mène au dossier
            dossier_full_path = root + "/" + dossier
            # on substitue les éventuels \ par /
            dossier_full_path = dossier_full_path.replace("\\", "/")
            # est-ce que l'on détecte dans dossier_full_path la pattern inputValue
            # l'expression régulière cherche après un nombre suivi d'un nombre suivi de la lettre P majuscule suivi d'une série de digit(s) suivi de quelque chose
            # le fait de mettre une parenthèse autour => premier groupe de match
            # donc si le dossier s'appelle 21P0023 - Tole sole DXF
            # un digit suivi d'un digit suivi de P suivi de digits suivi d'autre chose
            # le premier match group sera ce qui est juste après le P et uniquement les digits contigus

            rex = re.compile(r"\d\dP(\d*)(.*)", re.S | re.M)
            match = rex.match(dossier)
            if match:
                if int(match.groups()[0])==int(inputValue):
                  # explorer would choke on forward slashes
                  # path = os.path.normpath(dossier_full_path+"/02-Plans")
                  path = os.path.normpath(dossier_full_path)
                  if (os.path.isdir(path)):
                      pass
                  else:
                      path = os.path.normpath(dossier_full_path)
                  print("* %s" % (path))
                  if os.path.isdir(path):
                      subprocess.run([FILEBROWSER_PATH, path])
                  elif os.path.isfile(path):
                      subprocess.run([FILEBROWSER_PATH, '/select,', os.path.normpath(path)])
                  # d_names est une liste contenant tous les dossiers à scruter
                  # en invoquant .clear() on vide la liste...
                  d_names.clear()




#Caractéristique du widget tk
root.title('Arcalu 2.0')
root.geometry('500x180')
root.config(bg='grey')


# SpinBox pour la sélection de l'année.
sp = Spinbox(root, from_=21, to=50, width=2, font='Arial 15 bold')
# supprime entièrement la case valeur
sp.delete(0, 5)
# insère la valeur défaut, donc la variable year
sp.insert(0, year)
# Positionne la spinbox la fenêtre graphique
sp.pack(padx=10, pady=10)

# Défini les caractéristiques de la fenêtre de saisie
textBox = Text(root, height=1, width=6, font='Arial 30 bold')
# Permet de position la textBox dans la fenêtre graphique
textBox.pack(padx=20, pady=20)
# Permet de forcer la saisie dès que l'application s'ouvre
textBox.focus_set()

buttonCommit = Button(root, height=1, width=10, text="Commit",
                      command=lambda: retrieve_input())
# RADIO BUTTONS


# FIN RADIO BUTTONS
buttonCommit.pack()

mainloop()

