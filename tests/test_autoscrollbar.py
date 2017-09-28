from tkfilebrowser.autoscrollbar import AutoScrollbar
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestAutoScrollbar(BaseWidgetTest):
    def test_autoscrollbar_init(self):
        AutoScrollbar(self.window)
        self.window.update()

    def test_autoscrollbar_methods(self):
        scroll = AutoScrollbar(self.window, orient='vertical')
        # pack layout
        with self.assertRaises(tk.TclError):
            scroll.pack(side='right', fill='y')
        self.window.update()
        # place layout
        with self.assertRaises(tk.TclError):
            scroll.place(anchor='ne', relx=1, rely=0, relheight=1)
        self.window.update()
        # grid layout
        scroll.grid(row=0, column=1, sticky='ns')
        self.window.update()
        scroll.set(-0.1, 1.1)
        self.window.update()
        self.assertFalse(scroll.winfo_ismapped())
        scroll.set(0.1, 0.8)
        self.window.update()
        self.window.update()
        self.assertTrue(scroll.winfo_ismapped())
