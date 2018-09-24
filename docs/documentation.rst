Documentation
=============

Functions
---------

- *askopendirname*

    Allow the user to choose a single directory. The absolute path of the
    chosen directory is returned. If the user cancels, an empty string is
    returned.
    
    Syntax:
    
    ::
        
        askopendirname(parent=None, title=_("Open"), **kwargs)

- *askopendirnames*

    Allow the user to choose multiple directories. A tuple containing the absolute
    path of the chosen directories is returned. If the user cancels,
    an empty tuple is returned.    
    
    Syntax:
    
    ::
        
        askopendirnames(parent=None, title=_("Open"), **kwargs)
        
- *skopenfilename*

    Allow the user to choose a single file. The absolute path of the
    chosen file is returned. If the user cancels, an empty string is
    returned.    
    
    Syntax:
    
    ::
        
        askopenfilename(parent=None, title=_("Open"), **kwargs)

- *askopenfilenames*

    Allow the user to choose multiple files. A tuple containing the absolute
    path of the chosen files is returned. If the user cancels,
    an empty tuple is returned.    
    
    Syntax:
    
    ::
    
        askopenfilenames(parent=None, title=_("Open"), **kwargs)

- *asksaveasfilename*

    Allow the user to choose a file path. The file may not exist but
    the path to its directory does. If the file already exists, the user
    is asked to confirm its replacement.

    Additional option:
    
        defaultext : str (e.g. .png)
            extension added to filename if none is given (default is none)    
    
    Syntax:
    
    ::
        
        asksaveasfilename(parent=None, title=_("Save As"), **kwargs)
            

Optional keywords arguments common to all functions
---------------------------------------------------

    parent : Tk or Toplevel instance
        parent window

    title : str
        the title of the filebrowser window

    initialdir : str
        directory whose content is initially displayed

    initialfile : str
        initially selected item (just the name, not the full path)

    filetypes : list ``[("name", "*.ext1|*.ext2|.."), ...]``
      only the files of given filetype will be displayed,
      e.g. to allow the user to switch between displaying only PNG or JPG
      pictures or dispalying all files:
      filtypes=[("Pictures", "\*.png|\*.PNG|\*.jpg|\*.JPG'), ("All files", "\*")]

    okbuttontext : str
        text displayed on the validate button, if None, the
        default text corresponding to the mode is used (either "Open" or "Save")

    cancelbuttontext : str
        text displayed on the button that cancels the selection.

    foldercreation : bool
        enable the user to create new folders if True (default)
