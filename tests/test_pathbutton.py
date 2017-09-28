from tkfilebrowser.path_button import PathButton
from tests import BaseWidgetTest
try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk


class TestPathButton(BaseWidgetTest):
    def test_pathbutton_init(self):
        var = tk.StringVar(self.window)
        pb = PathButton(self.window, var, 'test')
        pb.pack()
        self.window.update()

    def test_pathbutton_methods(self):
        var = tk.StringVar(self.window)
        pb1 = PathButton(self.window, var, 'test1')
        pb2 = PathButton(self.window, var, 'test2')
        self.window.update()

        self.assertEqual(pb1.get_value(), 'test1')
        self.assertEqual(pb2.get_value(), 'test2')

        var.set('test1')
        self.assertIn('selected', pb1.state())
        self.assertNotIn('selected', pb2.state())
        pb2.on_press(None)
        self.window.update()
        self.assertIn('selected', pb2.state())
        self.assertNotIn('selected', pb1.state())

        try:
            n = len(var.trace_info())
        except AttributeError:
            # fallback to old method
            n = len(var.trace_vinfo())
        self.assertEqual(n, 2)
        pb2.destroy()
        try:
            n = len(var.trace_info())
        except AttributeError:
            # fallback to old method
            n = len(var.trace_vinfo())
        self.assertEqual(n, 1)


