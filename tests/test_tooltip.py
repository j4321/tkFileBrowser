from tkfilebrowser.tooltip import Tooltip, TooltipTreeWrapper
from tests import BaseWidgetTest, TestEvent
from pynput.mouse import Controller
try:
    import ttk
except ImportError:
    from tkinter import ttk


class TestTooltip(BaseWidgetTest):
    def test_tooltip(self):
        t = Tooltip(self.window, background='white', foreground='black')
        self.window.update()
        t.configure(text='Hello', background='black', foreground='white',
                    image=None, alpha=0.75)


class TestTooltipTreeWrapper(BaseWidgetTest):
    def test_tooltiptreewrapper(self):
        tree = ttk.Treeview(self.window, show='tree')
        tree.pack()
        tree.insert("", "end", "1", text="item 1")
        tree.insert("", "end", "2", text="item 2")
        self.window.update()
        tw = TooltipTreeWrapper(tree, background='white', foreground='black')
        tw.add_tooltip("1", "tooltip 1")
        tw.add_tooltip("2", "tooltip 2")
        self.window.update()
        tw._on_motion(TestEvent(x=10, y=10))
        x, y = tree.winfo_rootx(), tree.winfo_rooty()
        mouse_controller = Controller()
        mouse_controller.position = (x + 10, y + 10)
        tw.display_tooltip()
        tw._on_motion(TestEvent(x=10, y=10))
