# -*- coding: utf-8 -*-
"""
tkfilebrowser - Alternative to filedialog for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkfilebrowser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkfilebrowser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


The icons are modified versions of icons from the elementary project
(the xfce fork to be precise https://github.com/shimmerproject/elementary-xfce)
Copyright 2007-2013 elementary LLC.


Constants and functions
"""
print('ok')


import locale
import time
import os
from math import log, floor

try:
    import tkinter as tk
    from tkinter import ttk
    from tkinter.messagebox import askyesnocancel, showerror
    from urllib.parse import unquote
except ImportError:
    import Tkinter as tk
    import ttk
    from tkMessageBox import askyesnocancel, showerror
    from urllib import unquote
    import sys
    reload(sys)
    sys.setdefaultencoding('utf8')

PATH = os.path.dirname(__file__)

LOCAL_PATH = os.path.join(os.path.expanduser('~'), '.config', 'tkfilebrowser')

if not os.path.exists(LOCAL_PATH):
    try:
        if not os.path.exists(os.path.join(os.path.expanduser('~'), '.config')):
            os.mkdir(os.path.join(os.path.expanduser('~'), '.config'))
        os.mkdir(LOCAL_PATH)
    except Exception:
        # avoid raising error if the path is not writtable
        pass

RECENT_FILES = os.path.join(LOCAL_PATH, 'recent_files')

# ---  images
IM_HOME = os.path.join(PATH, "images", "home.png")
IM_FOLDER = os.path.join(PATH, "images", "dossier.png")
IM_FOLDER_LINK = os.path.join(PATH, "images", "dossier_link.png")
IM_NEW = os.path.join(PATH, "images", "new_folder.png")
IM_FILE = os.path.join(PATH, "images", "file.png")
IM_FILE_LINK = os.path.join(PATH, "images", "file_link.png")
IM_DRIVE = os.path.join(PATH, "images", "drive.png")
IM_RECENT = os.path.join(PATH, "images", "recent.png")
IM_RECENT_24 = os.path.join(PATH, "images", "recent_24.png")


# ---  translation
lang = locale.getdefaultlocale()[0][:2]

EN = {}
FR = {"B": "octets", "MB": "Mo", "kB": "ko", "GB": "Go", "TB": "To",
      "Name: ": "Nom : ", "Folder: ": "Dossier : ", "Size": "Taille",
      "Name": "Nom", "Modified": "Modifié", "Save": "Enregistrer",
      "Open": "Ouvrir", "Cancel": "Annuler", "Location": "Emplacement",
      "Today": "Aujourd'hui", "Confirmation": "Confirmation",
      "Error": "Erreur",
      "The file {file} already exists, do you want to replace it?": "Le fichier {file} existe déjà, voulez-vous le remplacer ?",
      "Shortcuts": "Raccourcis", "Save As": "Enregistrer sous",
      "Recent": "Récents", "Recently used": "Récemment utilisés"}
LANGUAGES = {"fr": FR, "en": EN}
if lang == "fr":
    TR = LANGUAGES["fr"]
else:
    TR = LANGUAGES["en"]


def _(text):
    """ translation function """
    return TR.get(text, text)


SIZES = [_("B"), _("kB"), _("MB"), _("GB"), _("TB")]

# ---  locale settings for dates
locale.setlocale(locale.LC_ALL, "")
TODAY = time.strftime("%x")
YEAR = time.strftime("%Y")
DAY = int(time.strftime("%j"))


# ---  functions
def add_trace(variable, mode, callback):
    """
    Add trace to variable.

    Ensure compatibility with old and new trace method.
    mode: "read", "write", "unset" (new syntax)
    """
    try:
        return variable.trace_add(mode, callback)
    except AttributeError:
        # fallback to old method
        return variable.trace(mode[0], callback)


def remove_trace(variable, mode, cbname):
    """
    Remove trace from variable.

    Ensure compatibility with old and new trace method.
    mode: "read", "write", "unset" (new syntax)
    """
    try:
        variable.trace_remove(mode, cbname)
    except AttributeError:
        # fallback to old method
        variable.trace_vdelete(mode[0], cbname)


def get_modification_date(file):
    """Return the modification date of file."""
    tps = time.localtime(os.path.getmtime(file))
    date = time.strftime("%x", tps)
    if date == TODAY:
        date = _("Today") + time.strftime(" %H:%M", tps)
    elif time.strftime("%Y", tps) == YEAR and (DAY - int(time.strftime("%j", tps))) < 7:
        date = time.strftime("%A %H:%M", tps)
    return date


def get_size(file):
    """Return the size of file."""
    size_o = os.path.getsize(file)
    if size_o > 0:
        m = int(floor(log(size_o) / log(1024)))
        if m < len(SIZES):
            unit = SIZES[m]
            s = size_o / (1024 ** m)
        else:
            unit = SIZES[-1]
            s = size_o / (1024**(len(SIZES) - 1))
        size = "%s %s" % (locale.format("%.1f", s), unit)
    else:
        size = "0 " + _("B")
    return size


def display_modification_date(mtime):
    """Return the modification date of file."""
    tps = time.localtime(mtime)
    date = time.strftime("%x", tps)
    if date == TODAY:
        date = _("Today") + time.strftime(" %H:%M", tps)
    elif time.strftime("%Y", tps) == YEAR and (DAY - int(time.strftime("%j", tps))) < 7:
        date = time.strftime("%A %H:%M", tps)
    return date


def display_size(size_o):
    """Return the size of file."""
    if size_o > 0:
        m = int(floor(log(size_o) / log(1024)))
        if m < len(SIZES):
            unit = SIZES[m]
            s = size_o / (1024 ** m)
        else:
            unit = SIZES[-1]
            s = size_o / (1024**(len(SIZES) - 1))
        size = "%s %s" % (locale.format("%.1f", s), unit)
    else:
        size = "0 " + _("B")
    return size


def key_sort_files(file):
    return file.is_file(), file.name.lower()

