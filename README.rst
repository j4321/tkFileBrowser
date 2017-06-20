tkFileBrowser
=============

tkFileBrowser is an alternative to tkinter.filedialog that allows the
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

Requirements
------------

- Linux
- Python 3 with tkinter + ttk


Installation
------------

With pip:

::

    $ pip3 install tkFileBrowser

Documentation
-------------

* Optional keywords arguments common to each function

    - parent: parent window

    - title: the title of the filebrowser window

    - initialdir: directory whose content is initially displayed

    - initialfile: initially selected item (just the name, not the full path)

    - filetypes list: [("name", "\*.ext1|\*.ext2|.."), ...]
      only the files of given filetype will be displayed,
      e.g. to allow the user to switch between displaying only PNG or JPG
      pictures or dispalying all files:
      filtypes=[("Pictures", "\*.png|\*.PNG|\*.jpg|\*.JPG'), ("All files", "\*")]

    - okbuttontext: text displayed on the validate button, if None, the
      default text corresponding to the mode is used (either "Open" or "Save")

    - cancelbuttontext: text displayed on the button that cancels the
      selection.

* askopendirname

    Allow the user to choose a single directory. The absolute path of the
    chosen directory is returned. If the user cancels, an empty string is
    returned.

* askopendirnames

    Allow the user to choose multiple directories. A tuple containing the absolute
    path of the chosen directories is returned. If the user cancels,
    an empty tuple is returned.

* askopenfilename

    Allow the user to choose a single file. The absolute path of the
    chosen file is returned. If the user cancels, an empty string is
    returned.


* askopenfilenames

    Allow the user to choose multiple files. A tuple containing the absolute
    path of the chosen files is returned. If the user cancels,
    an empty tuple is returned.

* asksaveasfilename

    Allow the user to choose a file path. The file may not exist but
    the path to its directory does. If the file already exists, the user
    is asked to confirm its replacement.

    Additional option:
        - defaultext: extension added to filename if none is given (default is none)

Changelog
---------

- tkFileBrowser 1.1.3
    * Correct bug: grey/white color alternance not respected after sorting
    * Add __main__.py with an example
    * Add recent files shortcut
    * Make the text of the validate and cancel buttons customizable

- tkFileBrowser 1.1.2
    * Add tooltips to display the full path of the shortcut if the mouse stays
      long enough over it.
    * Correct bug: style of browser treeview applied to parent

- tkFileBrowser 1.1.1
    * Correct bug: key browsing did not work with capital letters
    * Add specific icons for symlinks
    * Add handling of symlinks, the real path is returned instead of the link path

- tkFileBrowser 1.1.0
    * Correct bug concerning the initialfile argument
    * Add column sorting (by name, size, modification date)

- tkFileBrowser 1.0.1
    * Set default filebrowser parent to None as for the usual filedialogs
      and messageboxes.

- tkFileBrowser 1.0.0
    * Initial version


Example
=======

.. code:: python

    import tkinter as tk
    import tkinter.ttk as ttk
    from tkFileBrowser import askopendirnames, asksaveasfilename

    root = tk.Tk()

    def c_open():
        rep = askopendirnames(parent=root)
        print(rep)

    def c_save():
        rep = asksaveasfilename(parent=root, defaultext=".png",
                                filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), ("All files", "*")])
        print(rep)

    ttk.Button(root, text="Open folders", command=c_open).pack()
    ttk.Button(root, text="Save file", command=c_save).pack()

    root.mainloop()




