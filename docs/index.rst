.. tkfilebrowser documentation master file, created by
   sphinx-quickstart on Mon Sep 24 22:37:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tkfilebrowser
=============

|Release|_ |Linux| |Travis| |Codecov| |License|

tkfilebrowser is an alternative to tkinter.filedialog that allows the
user to select files or directories. The GUI is written with tkinter but
the look is closer to GTK and the application uses GTK bookmarks (the
one displayed in nautilus or thunar for instance). This filebrowser
supports new directory creation and filtype filtering.

This module contains a general `FileBrowser` class which implements the
filebrowser and the following functions, similar to the one in filedialog:

    * `askopenfilename` that allow the selection of a single file

    * `askopenfilenames` that allow the selection of multiple files

    * `askopendirname` that allow the selection a single folder

    * `askopendirnames` that allow the selection of multiple folders

    * `asksaveasfilename` that returns a single filename and give a warning if the file already exists
    
Project page: https://github.com/j4321/tkFileBrowser

.. toctree::
   :maxdepth: 4
   :caption: Contents:

   installation
   example
   documentation
   changelog



.. |Release| image:: https://badge.fury.io/py/tkfilebrowser.svg
    :alt: Latest Release
.. _Release:  https://pypi.org/project/tkfilebrowser/
.. |Linux| image:: https://img.shields.io/badge/platform-Linux-blue.svg
    :alt: Platform
.. |Travis| image:: https://travis-ci.org/j4321/tkFileBrowser.svg?branch=master
    :target: https://travis-ci.org/j4321/tkFileBrowser
    :alt: Travis CI Build Status
.. |Codecov| image:: https://codecov.io/gh/j4321/tkFileBrowser/branch/master/graph/badge.svg
    :target: https://codecov.io/gh/j4321/tkFileBrowser
    :alt: Code coverage
.. |License| image:: https://img.shields.io/github/license/j4321/tkFileBrowser.svg
    :target: https://www.gnu.org/licenses/gpl-3.0.en.html
    :alt: License
