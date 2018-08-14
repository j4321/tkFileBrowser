# -*- coding: utf-8 -*-
"""
tkfilebrowser - Alternative to filedialog for Tkinter
Copyright 2017-2018 Juliette Monsel <j_4321@protonmail.com>

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


Functions
"""


from tkfilebrowser.constants import _
from tkfilebrowser.filebrowser import FileBrowser


def askopendirname(parent=None, title=_("Open"), **kwargs):
    """
    Return '' or the absolute path of the chosen directory.

    Options:
        * initialdir: initial folder whose content is displayed
        * initialfile: initial selected item (just the name, not the full path)
        * filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
        * okbuttontext: text displayed on the validate button, if None, the
          default text corresponding to the mode is used (either Open or Save)
        * cancelbuttontext: text displayed on the button that cancels the
          selection.
        * foldercreation: enable the user to create new folders if True (default)
    """
    dialog = FileBrowser(parent, mode="opendir", multiple_selection=False,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()


def askopendirnames(parent=None, title=_("Open"), **kwargs):
    """
    Return () or the tuple of the absolute paths of the chosen directories

    Options:
        * initialdir: initial folder whose content is displayed
        * initialfile: initial selected item (just the name, not the full path)
        * filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
        * okbuttontext: text displayed on the validate button, if None, the
          default text corresponding to the mode is used (either Open or Save)
        * cancelbuttontext: text displayed on the button that cancels the
          selection.
        * foldercreation: enable the user to create new folders if True (default)
    """
    dialog = FileBrowser(parent, mode="opendir", multiple_selection=True,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    res = dialog.get_result()
    if not res:  # type consistency: always return a tuple
        res = ()
    return res


def askopenfilename(parent=None, title=_("Open"), **kwargs):
    """
    Return '' or the absolute path of the chosen file

    Options:
        * initialdir: initial folder whose content is displayed
        * initialfile: initial selected item (just the name, not the full path)
        * filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
        * okbuttontext: text displayed on the validate button, if None, the
          default text corresponding to the mode is used (either Open or Save)
        * cancelbuttontext: text displayed on the button that cancels the
          selection.
        * foldercreation: enable the user to create new folders if True (default)
    """
    dialog = FileBrowser(parent, mode="openfile", multiple_selection=False,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()


def askopenfilenames(parent=None, title=_("Open"), **kwargs):
    """
    Return () or the tuple of the absolute paths of the chosen files

    Options:
        * initialdir: initial folder whose content is displayed
        * initialfile: initial selected item (just the name, not the full path)
        * filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
        * okbuttontext: text displayed on the validate button, if None, the
          default text corresponding to the mode is used (either Open or Save)
        * cancelbuttontext: text displayed on the button that cancels the
          selection.
        * foldercreation: enable the user to create new folders if True (default)
    """
    dialog = FileBrowser(parent, mode="openfile", multiple_selection=True,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    res = dialog.get_result()
    if not res:  # type consistency: always return a tuple
        res = ()
    return res


def asksaveasfilename(parent=None, title=_("Save As"), **kwargs):
    """
    Return '' or the chosen absolute path (the file might not exist)

    Options:
        * initialdir: initial folder whose content is displayed
        * initialfile: initial selected item (just the name, not the full path)
        * defaultext: extension added to filename if none is given
        * filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
        * okbuttontext: text displayed on the validate button, if None, the
          default text corresponding to the mode is used (either Open or Save)
        * cancelbuttontext: text displayed on the button that cancels the
          selection.
        * foldercreation: enable the user to create new folders if True (default)
    """
    dialog = FileBrowser(parent, mode="save", title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()
