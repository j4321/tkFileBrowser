import tkinter as tk
import tkinter.ttk as ttk
import tkFileBrowser as tkb
from ttkthemes import ThemedTk

root = ThemedTk()

def c_open():
    rep = tkb.askopendirnames(parent=root, foldercreation=False, title='Test',
                              okbuttontext='Select')
    print(rep)

def c_save():
    rep = tkb.asksaveasfilename(parent=root, defaultext=".png",
                            filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), ("All files", "*")])
    print(rep)
s = ttk.Style(root)
s.theme_use('black')
s.configure('Treeview', fieldbackground='gray30', background='gray30')

c = ttk.Combobox(root, values=s.theme_names())
c.pack()
c.set('default')
c.bind("<<ComboboxSelected>>", lambda e: s.theme_use(c.get()))

ttk.Button(root, text="Open folders", command=c_open).pack()
ttk.Button(root, text="Open folder", command=lambda: print(tkb.askopendirname(parent=root))).pack()
ttk.Button(root, text="Open files", command=lambda: print(tkb.askopenfilenames(parent=root))).pack()
ttk.Button(root, text="Open file", command=lambda: print(tkb.askopenfilename(parent=root, filetypes=[("IMG", "*.png|*.jpg"), ("all", "*")]))).pack()
ttk.Button(root, text="Save file", command=c_save).pack()

root.mainloop()

