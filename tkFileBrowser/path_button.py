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


Path bar button class
"""


from tkFileBrowser.constants import add_trace, ttk


class PathButton(ttk.Button):
    """ Toggle button class to make the path bar """

    def __init__(self, parent, variable, value, **kwargs):
        ttk.Button.__init__(self, parent, **kwargs)
        self.variable = variable
        self.value = value
        self.style = ttk.Style(self)
        self.style.configure("%s.TButton" % value, padding=2)
        self.selected_bg = self.style.lookup("TButton", "background",
                                             ("pressed",))
        self.normal_bg = self.style.lookup("TButton", "background")
        self.configure(style="%s.TButton" % value)
        add_trace(self.variable, "write", self.var_change)
        self.bind("<Button-1>", self.on_press)

    def on_press(self, event):
        self.variable.set(self.value)

    def get_value(self):
        return self.value

    def var_change(self, *args):
        self.master.update()
        self.master.update_idletasks()
        if self.variable.get() == self.value:
            self.style.configure("%s.TButton" % self.value,
                                 background=self.selected_bg,
                                 font="TkDefaultFont 9 bold")
        else:
            self.style.configure("%s.TButton" % self.value,
                                 font="TkDefaultFont",
                                 background=self.normal_bg)
