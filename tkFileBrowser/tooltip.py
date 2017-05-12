#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
tkFileBrowser - Alternative to filedialog for Tkinter
Copyright 2017 Juliette Monsel <j_4321@protonmail.com>

tkFileBrowser is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

tkFileBrowser is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <http://www.gnu.org/licenses/>.


Tooltip and TooltipTreeWrapper classes to display the full path of a shortcut
when the mouse stays over long enough
"""

from tkinter import Toplevel, Tk, TclError
from tkinter.ttk import Label, Style, Treeview

class Tooltip(Toplevel):
    def __init__(self, parent, **kwargs):
        Toplevel.__init__(self, parent)
        if 'title' in kwargs:
            self.title(kwargs['title'])
        self.transient(parent)
        self.attributes('-type', 'tooltip')
        self.attributes('-alpha', kwargs.get('alpha', 0.8))
        self.overrideredirect(True)
        self.configure(padx=kwargs.get('padx', 4))
        self.configure(pady=kwargs.get('pady', 4))

        self.style = Style(self)
        if 'background' in kwargs:
            bg = kwargs['background']
            self.configure(background=bg)
            self.style.configure('tooltip.TLabel', background=bg)
        if 'foreground' in kwargs:
            self.style.configure('tooltip.TLabel', foreground=kwargs['foreground'])

        self.im = kwargs.get('image', None)
        self.label = Label(self, text=kwargs.get('text', ''), image=self.im,
                           style='tooltip.TLabel',
                           compound=kwargs.get('compound', 'left'))
        self.label.pack()

    def configure(self, **kwargs):
        if 'text' in kwargs:
            self.label.configure(text=kwargs.pop('text'))
        if 'image' in kwargs:
            self.label.configure(image=kwargs.pop('image'))
        if 'background' in kwargs:
            self.style.configure('tooltip.TLabel', background=kwargs['background'])
        if 'foreground' in kwargs:
            fg = kwargs.pop('foreground')
            self.style.configure('tooltip.TLabel', foreground=fg)
        if 'alpha' in kwargs:
            self.attributes('-alpha', kwargs.pop('alpha'))
        Toplevel.configure(self, **kwargs)


class TooltipTreeWrapper:

    def __init__(self, tree, delay=1500, **kwargs):
        self.tree = tree
        self.delay = delay
        self._timer_id = ''
        self.tooltip_text = {}
        self.tooltip = Tooltip(tree, **kwargs)
        self.tooltip.withdraw()
        self.current_item = None

        self.tree.bind('<Motion>', self._on_motion)
        self.tree.bind('<Leave>', lambda e: self.tree.after_cancel(self._timer_id))


    def add_tooltip(self, item, text):
        self.tooltip_text[item] = text

    def _on_motion(self, event):
        if self.tooltip.winfo_ismapped():
            x, y = self.tree.winfo_pointerxy()
            if self.tree.winfo_containing(x, y) != self.tooltip:
                if self.tree.identify_row(y - self.tree.winfo_rooty()):
                    self.tooltip.withdraw()
                    self.current_item = None
        else:
            self.tree.after_cancel(self._timer_id)
            self._timer_id = self.tree.after(self.delay, self.display_tooltip)

    def display_tooltip(self):
        item = self.tree.identify_row(self.tree.winfo_pointery() - self.tree.winfo_rooty())
        text = self.tooltip_text.get(item, '')
        self.current_item = item
        if text:
            self.tooltip.configure(text=text)
            self.tooltip.deiconify()
            x = self.tree.winfo_pointerx() + 14
            y = self.tree.winfo_rooty() + self.tree.bbox(item)[1] + self.tree.bbox(item)[3]
            self.tooltip.geometry('+%i+%i' % (x, y))

if __name__ == '__main__':

    root = Tk()
    tree = Treeview(root)
    tree.pack()
    tree.insert("", 0, text='0')
    tree.insert("", 0, text='1')
    tree.insert("", 0, text='2')
    w = TooltipTreeWrapper(tree, background='black', foreground='white')
    for item in tree.get_children(''):
        w.add_tooltip(item, 'hello ' + item)
    root.mainloop()