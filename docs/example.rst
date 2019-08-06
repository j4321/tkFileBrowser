Example
=======

.. code:: python

    try:
        import tkinter as tk
        import tkinter.ttk as ttk
        from tkinter import filedialog
    except ImportError:
        import Tkinter as tk
        import ttk
        import tkFileDialog as filedialog
    from tkfilebrowser import askopendirname, askopenfilenames, asksaveasfilename, askopenpathnames


    root = tk.Tk()

    style = ttk.Style(root)
    style.theme_use("clam")


    def c_open_file_old():
        rep = filedialog.askopenfilenames(parent=root, 
                                          initialdir='/', 
                                          initialfile='tmp',
                                          filetypes=[("PNG", "*.png"), 
                                                     ("JPEG", "*.jpg"), 
                                                     ("All files", "*")])
        print(rep)


    def c_open_dir_old():
        rep = filedialog.askdirectory(parent=root, initialdir='/tmp')
        print(rep)


    def c_save_old():
        rep = filedialog.asksaveasfilename(parent=root, 
                                           defaultextension=".png", 
                                           initialdir='/tmp', 
                                           initialfile='image.png',
                                           filetypes=[("PNG", "*.png"), 
                                                      ("JPEG", "*.jpg"), 
                                                      ("All files", "*")])
        print(rep)


    def c_open_file():
        rep = askopenfilenames(parent=root, 
                               initialdir='/', 
                               initialfile='tmp',
                               filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), 
                                          ("All files", "*")])
        print(rep)


    def c_open_dir():
        rep = askopendirname(parent=root, 
                             initialdir='/', 
                             initialfile='tmp')
        print(rep)


    def c_save():
        rep = asksaveasfilename(parent=root, 
                                defaultext=".png", 
                                initialdir='/tmp', 
                                initialfile='image.png',
                                filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), 
                                           ("All files", "*")])
        print(rep)
        
    
    def c_path():
        rep = askopenpathnames(parent=root, initialdir='/', initialfile='tmp')
        print(rep)


    ttk.Label(root, text='Default dialogs').grid(row=0, column=0, 
                                                 padx=4, pady=4, 
                                                 sticky='ew')
    ttk.Label(root, text='tkfilebrowser dialogs').grid(row=0, column=1, 
                                                       padx=4, pady=4, 
                                                       sticky='ew')
    ttk.Button(root, text="Open files", command=c_open_file_old).grid(row=1, column=0, 
                                                                      padx=4, pady=4, 
                                                                      sticky='ew')
    ttk.Button(root, text="Open folder", command=c_open_dir_old).grid(row=2, column=0, 
                                                                      padx=4, pady=4, 
                                                                      sticky='ew')
    ttk.Button(root, text="Save file", command=c_save_old).grid(row=3, column=0, 
                                                                padx=4, pady=4, 
                                                                sticky='ew')
    ttk.Button(root, text="Open files", command=c_open_file).grid(row=1, column=1, 
                                                                  padx=4, pady=4, 
                                                                  sticky='ew')
    ttk.Button(root, text="Open folder", command=c_open_dir).grid(row=2, column=1,
                                                                  padx=4, pady=4, 
                                                                  sticky='ew')
    ttk.Button(root, text="Save file", command=c_save).grid(row=3, column=1,
                                                            padx=4, pady=4, 
                                                            sticky='ew')
    ttk.Button(root, text="Open paths", command=c_path).grid(row=4, column=1, 
                                                             padx=4, pady=4, 
                                                             sticky='ew')


    root.mainloop()
