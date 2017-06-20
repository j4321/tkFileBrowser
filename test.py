import tkinter as tk
import tkinter.ttk as ttk
import tkFileBrowser as tkb

root = tk.Tk()

def c_open():
    rep = tkb.askopendirnames(parent=root)
    print(rep)

def c_save():
    rep = tkb.asksaveasfilename(parent=root, defaultext=".png",
                            filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), ("All files", "*")])
    print(rep)
s = ttk.Style(root)
s.theme_use("clam")
print(s.layout("TButton"))
ttk.Button(root, text="Open folders", command=c_open).pack()
ttk.Button(root, text="Open folder", command=lambda: print(tkb.askopendirname(parent=root))).pack()
ttk.Button(root, text="Open files", command=lambda: print(tkb.askopenfilenames(parent=root))).pack()
ttk.Button(root, text="Open file", command=lambda: print(tkb.askopenfilename(parent=root, filetypes=[("IMG", "*.png|*.jpg"), ("all", "*")]))).pack()
ttk.Button(root, text="Save file", command=c_save).pack()

root.mainloop()

