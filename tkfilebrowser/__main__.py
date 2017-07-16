# -*- coding: utf-8 -*-
"""
tkfilebrowser - Alternative to filedialog for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

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


Example
"""

from tkfilebrowser.constants import tk, ttk
from tkfilebrowser import askopendirnames, asksaveasfilename

root = tk.Tk()

style = ttk.Style(root)
style.theme_use("clam")


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
