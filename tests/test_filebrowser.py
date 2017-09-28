from tkfilebrowser.filebrowser import FileBrowser
from tests import BaseWidgetTest, TestEvent
try:
    import ttk
except ImportError:
    from tkinter import ttk


class TestFileBrowser(BaseWidgetTest):
    def test_filebrowser(self):
        fb = FileBrowser(self.window, initialdir=".", initialfile="", mode="opendir",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()
        fb = FileBrowser(self.window, initialdir=".", initialfile="", mode="openfile",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()
        fb = FileBrowser(self.window, initialdir=".", initialfile="", mode="save",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[("PNG", '*.png'), ('ALL', '*')],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()


