from tkFileBrowser.constants import tk, ttk
from tkFileBrowser import askopendirnames, asksaveasfilename
import ttkthemes

root = ttkthemes.ThemedTk()


def change_theme(event):
    s.theme_use(c.get())


def c_open():
    rep = askopendirnames(parent=root)
    print(rep)


def c_save():
    rep = asksaveasfilename(parent=root, defaultext=".png",
                            filetypes=[("Pictures", "*.png|*.jpg|*.JPG"), ("All files", "*")])
    print(rep)


s = ttk.Style(root)
s.theme_use('black')
c = ttk.Combobox(root, values=s.theme_names())
c.set('black')
#s.configure("Treeview", fieldbackground="gray30")
c.bind('<<ComboboxSelected>>', change_theme)
c.pack()
ttk.Button(root, text="Open folders", command=c_open).pack()
ttk.Button(root, text="Save file", command=c_save).pack()

root.mainloop()
