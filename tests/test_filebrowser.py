from tkfilebrowser.filebrowser import FileBrowser
from tests import BaseWidgetTest, TestEvent
try:
    import ttk
except ImportError:
    from tkinter import ttk
import os


class TestFileBrowser(BaseWidgetTest):
    def test_filebrowser_opendir(self):
        # --- multiple selection
        path = os.path.expanduser('~')
        fb = FileBrowser(self.window, initialdir=path, initialfile="test", mode="opendir",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.right_tree.focus_set()
        fb.event_generate('<Control-a>')
        self.window.update()
        self.window.update_idletasks()
        fb.validate()
        walk = os.walk(path)
        root, dirs, _ = walk.send(None)
#        res = list(fb.right_tree.selection())
        res = list(fb.get_result())
        res.sort()
        dirs = [os.path.join(root, d) for d in dirs]
        dirs.sort()
        self.assertEqual(res, dirs)
        # --- single selection
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="opendir",
                         multiple_selection=False, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.validate()
        self.assertTrue(os.path.isdir(fb.get_result()))

    def test_filebrowser_openfile(self):
        # --- multiple selection
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="openfile",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.event_generate('<Control-a>')
        self.window.update()
        fb.validate()
        walk = os.walk(os.path.abspath("."))
        root, _, files = walk.send(None)
        res = list(fb.get_result())
        res.sort()
        files = [os.path.join(root, d) for d in files]
        files.sort()
        self.assertEqual(res, files)
        # --- single selection
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="openfile",
                         multiple_selection=False, defaultext="",
                         title="Test", filetypes=[("PNG", '*.png'), ('ALL', '*')],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.validate()
        self.assertEqual(fb.get_result(), '')
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="openfile",
                         multiple_selection=False, defaultext="",
                         title="Test", filetypes=[("PNG", '*.png'), ('ALL', '*')],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        fb.validate()
        self.assertEqual(fb.get_result(), '')
        fb = FileBrowser(self.window, initialdir=".", initialfile="test", mode="openfile",
                         multiple_selection=False, defaultext="",
                         title="Test", filetypes=[],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=False)
        self.window.update()
        walk = os.walk(os.path.abspath("."))
        root, _, files = walk.send(None)
        files = fb.right_tree.tag_has('file')
        if files:
            fb.right_tree.selection_set(files[0])
            fb.validate()
            self.assertTrue(os.path.isfile(fb.get_result()))
        else:
            fb.validate()
            self.assertEqual(fb.get_result(), '')

    def test_filebrowser_save(self):
        fb = FileBrowser(self.window, initialdir="/", initialfile="test", mode="save",
                         multiple_selection=True, defaultext=".png",
                         title="Test", filetypes=[("PNG", '*.png'), ('ALL', '*')],
                         okbuttontext=None, cancelbuttontext="Cancel",
                         foldercreation=True)
        self.window.update()
        fb.validate()
        self.assertEqual(fb.get_result(), '/test.png')
