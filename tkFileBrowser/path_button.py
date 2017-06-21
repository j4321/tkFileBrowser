# -*- coding: utf-8 -*-
"""
Created on Sat Apr  8 11:24:51 2017

@author: tux
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
