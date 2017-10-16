from tkfilebrowser.filebrowser import FileBrowser
from tests import BaseWidgetTest, TestEvent
try:
    import ttk
except ImportError:
    from tkinter import ttk


class TestFileBrowser(BaseWidgetTest):
    def test_filebrowser(self):
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="opendir",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="openfile",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()
        fb = FileBrowser(self.window, initialdir="/", initialfile="test", mode="save",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[("PNG", '*.png'), ('ALL', '*')],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.destroy()


