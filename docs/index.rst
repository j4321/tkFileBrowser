.. tkfilebrowser documentation master file, created by
   sphinx-quickstart on Mon Sep 24 22:37:52 2018.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

tkfilebrowser
=============

|Release| |Linux| |Travis| |Codecov| |License| |Doc|

tkfilebrowser is an alternative to tkinter.filedialog that allows the
user to select files or directories. The GUI is written with tkinter but
the look is closer to GTK and the application uses GTK bookmarks (the
one displayed in nautilus or thunar for instance). This filebrowser
supports new directory creation and filtype filtering.

This module contains a general :class:`~tkfilebrowser.FileBrowser` class which implements the
filebrowser and the following functions, similar to the one in filedialog:

    * :func:`~tkfilebrowser.askopenfilename` that allow the selection of a single file

    * :func:`~tkfilebrowser.askopenfilenames` that allow the selection of multiple files

    * :func:`~tkfilebrowser.askopendirname` that allow the selection a single folder

    * :func:`~tkfilebrowser.askopendirnames` that allow the selection of multiple folders
    
    * :func:`~tkfilebrowser.askopendirname` that allow the selection a single file or folder

    * :func:`~tkfilebrowser.askopendirnames` that allow the selection of multiple files and folders

    * :func:`~tkfilebrowser.asksaveasfilename` that returns a single filename and give a warning if the file already exists
    
Project page: https://github.com/j4321/tkFileBrowser

.. toctree::
   :maxdepth: 1
   :caption: Contents:

   installation
   example
   documentation
   changelog
   genindex


.. |Release| image:: https://badge.fury.io/py/tkfilebrowser.svg
    :alt: Latest Release
    :target:  https://pypi.org/project/tkfilebrowser/
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
.. |Doc| image:: https://readthedocs.org/projects/tkfilebrowser/badge/?version=latest
    :target: https://tkfilebrowser.readthedocs.io/en/latest/?badge=latest
    :alt: Documentation Status
