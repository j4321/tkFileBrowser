from tkFileBrowser.constants import tk, ttk
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
