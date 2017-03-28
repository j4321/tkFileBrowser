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
"""

import os
import locale
import time
import psutil
from math import log10

from tkinter import Toplevel, PhotoImage, TclError, StringVar, Listbox, Menu
from tkinter.ttk import Treeview, Button, Label, Frame, Scrollbar, Entry
from tkinter.ttk import Style, PanedWindow, Menubutton
from tkinter.messagebox import askyesnocancel
from urllib.parse import unquote

PATH = os.path.dirname(__file__)

IM_HOME = os.path.join(PATH, "images", "home.png")
IM_FOLDER = os.path.join(PATH, "images", "dossier.png")
IM_NEW = os.path.join(PATH, "images", "new_folder.png")
IM_FILE = os.path.join(PATH, "images", "file.png")
IM_DRIVE = os.path.join(PATH, "images", "drive.png")

lang = locale.getdefaultlocale()[0][:2]

EN = {}
FR = {"B": "octets", "MB": "Mo", "kB": "ko", "GB": "Go", "TB": "To",
      "Name: ": "Nom : ", "Folder: ": "Dossier : ", "Size": "Taille",
      "Modified": "Modifié", "Save": "Enregistrer", "Open": "Ouvrir",
      "Cancel": "Annuler", "Confirmation": "Confirmation",
      "The file {file} already exists, do you want to replace it?": "Le fichier {file} existe déjà, voulez-vous le remplacer ?",
      "Shortcuts": "Raccourcis", "Save As": "Enregistrer sous"}
LANGUAGES = {"fr": FR, "en": EN}
if lang == "fr":
    TR = LANGUAGES["fr"]
else:
    TR = LANGUAGES["en"]


def _(text):
    """ translation function """
    return TR.get(text, text)


# locale settings for dates
locale.setlocale(locale.LC_ALL, "")
TODAY = time.strftime("%x")
YEAR = time.strftime("%Y")
DAY = int(time.strftime("%j"))


def add_trace(variable, mode, callback):
    """ ensure compatibility with old and new trace method
        mode: "read", "write", "unset" (new syntax)
    """
    try:
        variable.trace_add(mode, callback)
    except AttributeError:
        # fallback to old method
        variable.trace(mode[0], callback)


def get_modification_date(file):
    tps = time.localtime(os.path.getmtime(file))
    date = time.strftime("%x", tps)
    if date == TODAY:
        date = time.strftime("%H:%M", tps)
    elif time.strftime("%Y", tps) == YEAR and (DAY - int(time.strftime("%j", tps))) < 7:
        date = time.strftime("%A à %H:%M", tps)
    return date


SIZES = [(_("B"), 1), ("kB", 1e3), ("MB", 1e6), ("GB", 1e9), ("TB", 1e12)]


def get_size(file):
    size_o = os.path.getsize(file)
    if size_o > 0:
        m = int(log10(size_o)//3)
        if m < len(SIZES):
            unit, div = SIZES[m]
        else:
            unit, div = SIZES[-1]
        size = "%s %s" % (locale.format("%.1f", size_o/div), unit)
    else:
        size = "0" + _("B")
    return size


class AutoScrollbar(Scrollbar):
    """ a scrollbar that hides itself if it's not needed.  only
        works if you use the grid geometry manager. """

    def set(self, lo, hi):
        if float(lo) <= 0.0 and float(hi) >= 1.0:
            self.grid_remove()
        else:
            self.grid()
        Scrollbar.set(self, lo, hi)

    def pack(self, **kw):
        raise TclError("cannot use pack with this widget")

    def place(self, **kw):
        raise TclError("cannot use place with this widget")


class PathButton(Button):
    """ Toggle button class to make the path bar """

    def __init__(self, parent, variable, value, **kwargs):
        Button.__init__(self, parent, **kwargs)
        self.variable = variable
        self.value = value
        self.style = Style(self)
        self.style.configure("%s.TButton" % value, padding=2)
        self.selected_bg = self.style.lookup("TButton", "background",
                                             ("pressed",))
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
                                 background="lightgray")


class FileBrowser(Toplevel):
    def __init__(self, parent, initialdir="", initialfile="", mode="openfile",
                 multiple_selection=False, defaultext="", title="Filebrowser",
                 filetypes=[]):
        """ Create a filebrowser dialog.
            - initialdir: initial folder whose content is displayed
            - initialfile: initial selected item (just the name, not the full path)
            - mode: openfile, opendir or save
            - multiple_selection (open modes only): boolean, allow to select multiple files,
            - defaultext (save mode only): extension added to filename if none is given
            - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
              show only files of given filetype ("*" for all files)
        """
        Toplevel.__init__(self, parent)

        # keep track of folders to be able to move backward/foreward in history
        if initialdir:
            self.history = [initialdir]
        else:
            self.history = [os.path.expanduser("~")]
        self.hist_index = -1

        self.transient(parent)
        self.grab_set()
        self.protocol("WM_DELETE_WINDOW", self.quit)
        self.title(title)

        self.rowconfigure(2, weight=1)
        self.columnconfigure(0, weight=1)

        self.mode = mode
        self.result = ""

        # hidden files/folders visibility
        self.hide = False
        # hidden items
        self.hidden = ()

        # style
        style = Style(self)
        style.theme_use("clam")
        bg = "#E7E7E7"
        style.configure("left.Treeview", background=bg,
                        fieldbackground=bg)
        style.configure("Treeview.Heading", font="TkDefaultFont")
        style.configure("listbox.TFrame", background="white", relief="sunken")
        style.layout("Treeview.Heading",
                     [('Treeheading.cell', {'sticky': 'nswe'}),
                      ('Treeheading.border',
                       {'children': [('Treeheading.padding',
                                      {'children': [('Treeheading.image',
                                                     {'side': 'right', 'sticky': ''}),
                                                    ('Treeheading.text',
                                                     {'sticky': 'w'})],
                                       'sticky': 'nswe'})],
                        'sticky': 'nswe'})])

        # images
        self.im_file = PhotoImage(file=IM_FILE, master=self)
        self.im_folder = PhotoImage(file=IM_FOLDER, master=self)
        self.im_new = PhotoImage(file=IM_NEW, master=self)
        self.im_drive = PhotoImage(file=IM_DRIVE, master=self)
        self.im_home = PhotoImage(file=IM_HOME, master=self)

         # filetypes
        self.filetype = StringVar(self)
        self.filetypes = {}
        if filetypes:
            b_filetype = Menubutton(self, textvariable=self.filetype)
            self.menu = Menu(self, tearoff=False)
            for name, exts in filetypes:
                self.filetypes[name] = [ext.split("*")[-1].strip() for ext in exts.split("|")]
                self.menu.add_radiobutton(label=name, value=name,
                                          command=lambda: self.display_folder(self.history[self.hist_index]),
                                          variable=self.filetype)
            b_filetype.configure(menu=self.menu)
            b_filetype.grid(row=3, sticky="e", padx=10, pady=4)
            self.filetype.set(filetypes[0][0])
        else:
            self.filetypes[""] = [""]
            self.menu = None


        # path completion
        self.complete = self.register(self.completion)
        self.listbox_var = StringVar(self)
        self.listbox_frame = Frame(self, style="listbox.TFrame", borderwidth=1)
        self.listbox = Listbox(self.listbox_frame,
                               listvariable=self.listbox_var,
                               highlightthickness=0,
                               borderwidth=0,
                               selectbackground=style.lookup("Treeview",
                                                             "background",
                                                             ("selected",)))
        self.listbox.pack(expand=True, fill="x")

        # file name
        if mode == "save":
            self.defaultext = defaultext

            frame_name = Frame(self)
            frame_name.grid(row=0, pady=(10, 0), padx=10, sticky="ew")
            Label(frame_name, text=_("Name: ")).pack(side="left")
            self.entry = Entry(frame_name, validate="key",
                               validatecommand=(self.complete, "%d", "%S",
                                                "%i", "%s"))
            self.entry.pack(side="left", fill="x", expand=True)

            if initialfile:
                print(type(initialfile), initialfile, self.entry)
                self.entry.insert(0, initialfile)
        else:
            self.multiple_selection = multiple_selection

        # path bar
        self.path_var = StringVar(self)
        frame_bar = Frame(self)
        frame_bar.columnconfigure(0, weight=1)
        frame_bar.grid(row=1, sticky="ew", pady=10, padx=10)
        self.path_bar = Frame(frame_bar)
        self.path_bar.grid(row=0, column=0, sticky="ew")
        self.path_bar_buttons = []
        Button(frame_bar, image=self.im_new,
               command=self.create_folder).grid(row=0, column=1, sticky="e")
        if mode == "save":
            Label(self.path_bar, text=_("Folder: ")).grid(row=0, column=0)
        else:
            self.entry = Entry(frame_bar, validate="key",
                               validatecommand=(self.complete, "%d", "%S",
                                                "%i", "%s"))
            self.entry.grid(row=1, column=0, sticky="ew", padx=(0, 4),
                            pady=(10, 0))
            self.entry.grid_remove()
            self.entry.bind("<Escape>", self.toggle_path_entry)

        paned = PanedWindow(self, orient="horizontal")
        paned.grid(row=2, sticky="eswn", padx=10)

        # left pane
        left_pane = Frame(paned)
        left_pane.columnconfigure(0, weight=1)
        left_pane.rowconfigure(0, weight=1)

        paned.add(left_pane, weight=0)
        self.left_tree = Treeview(left_pane, selectmode="browse",
                                  style="left.Treeview")
        self.left_tree.column("#0", width=150)
        self.left_tree.heading("#0", text=_("Shortcuts"))
        self.left_tree.grid(row=0, column=0, sticky="sewn")
        self.left_tree.bind("<<TreeviewSelect>>", self.shortcut_select)

        scroll_left = AutoScrollbar(left_pane, command=self.left_tree.yview)
        scroll_left.grid(row=0, column=1, sticky="ns")
        self.left_tree.configure(yscrollcommand=scroll_left.set)

        # list devices and bookmarked locations
        devices = psutil.disk_partitions()

        for d in devices:
            m = d.mountpoint
            if m == "/":
                txt = "/"
            else:
                txt = os.path.split(m)[-1]
            self.left_tree.insert("", "end", iid=m, text=txt,
                                  image=self.im_drive)
        home = os.path.expanduser("~")
        self.left_tree.insert("", "end", iid=home, image=self.im_home,
                              text=os.path.split(home)[-1])
        path_bm = os.path.join(home, ".config", "gtk-3.0", "bookmarks")
        path_bm2 = os.path.join(home, ".gtk-bookmarks")  # old location
        if os.path.exists(path_bm):
            with open(path_bm) as f:
                bm = f.readlines()
        elif os.path.exists(path_bm2):
            with open(path_bm) as f:
                bm = f.readlines()
        else:
            bm = []
        bm = [unquote(ch).replace("file://", "").split() for ch in bm]
        for l in bm:
            if len(l) == 1:
                self.left_tree.insert("", "end", iid=l[0],
                                      text=os.path.split(l[0])[-1],
                                      image=self.im_folder)
            else:
                self.left_tree.insert("", "end", iid=l[0],
                                      text=l[1],
                                      image=self.im_folder)

        # right pane
        right_pane = Frame(paned)
        right_pane.columnconfigure(0, weight=1)
        right_pane.rowconfigure(0, weight=1)
        paned.add(right_pane, weight=1)

        if mode != "save" and multiple_selection:
            selectmode = "extended"
        else:
            selectmode = "browse"

        self.right_tree = Treeview(right_pane, selectmode=selectmode,
                                   columns=("size", "date"))
        self.right_tree.heading("#0", text=_("Name"))
        self.right_tree.heading("size", text=_("Size"))
        self.right_tree.heading("date", text=_("Modified"))
        self.right_tree.column("#0", width=250)
        self.right_tree.column("size", stretch=False, width=85)
        self.right_tree.column("date", stretch=False, width=115)
        self.right_tree.tag_configure("0", background="white")
        self.right_tree.tag_configure("1", background="#E7E7E7")
        self.right_tree.tag_configure("folder", image=self.im_folder)
        self.right_tree.tag_configure("file", image=self.im_file)
        self.right_tree.grid(row=0, column=0, sticky="eswn")

        self.right_tree.bind("<Double-1>", self.select)
        self.right_tree.bind("<Return>", self.select)
        self.right_tree.bind("<Left>", self.go_left)
        self.right_tree.bind("<Control-Shift-N>", self.create_folder)

        if mode == "opendir":
            self.right_tree.tag_configure("file", foreground="gray")
            self.right_tree.bind("<<TreeviewSelect>>",
                                 self.file_selection_opendir)
        elif mode == "openfile":
            self.right_tree.bind("<<TreeviewSelect>>",
                                 self.file_selection_openfile)
        else:
            self.right_tree.bind("<<TreeviewSelect>>",
                                 self.file_selection_save)
        self.right_tree.bind("<KeyPress>", self.key_browse_show)

        scroll_right = AutoScrollbar(right_pane, command=self.right_tree.yview)
        scroll_right.grid(row=0, column=1, sticky="ns")
        self.right_tree.configure(yscrollcommand=scroll_right.set)

        # buttons
        frame_buttons = Frame(self)
        frame_buttons.grid(row=4, sticky="ew", pady=10, padx=10)
        if mode == "save":
            text = _("Save")
        else:
            text = _("Open")
        Button(frame_buttons, text=text,
               command=self.validate).pack(side="right")
        Button(frame_buttons, text=_("Cancel"),
               command=self.quit).pack(side="right", padx=4)

        # key browsing entry
        self.key_browse_var = StringVar(self)
        self.key_browse_entry = Entry(self, textvariable=self.key_browse_var,
                                      width=10)
        add_trace(self.key_browse_var, "write", self.key_browse)
        self.key_browse_entry.bind("<FocusOut>", self.key_browse_hide)
        self.key_browse_entry.bind("<Escape>", self.key_browse_hide)
        self.key_browse_entry.bind("<Return>", self.key_browse_validate)
        # list of folders/files beginning by the letters inserted in self.key_browse_entry
        self.paths_beginning_by = []
        self.paths_beginning_by_index = 0  # current index in the list

        # initialization
        if not initialdir:
            initialdir = os.path.expanduser("~")

        self.display_folder(initialdir)
        initialpath = os.path.join(initialdir, initialfile)
        if initialpath in self.right_tree.get_children(""):
            self.right_tree.selection_add(initialpath)

        # bindings
        self.listbox.bind("<FocusOut>",
                          lambda e: self.listbox_frame.place_forget())

        self.entry.bind("<Down>", self.down)
        self.entry.bind("<Return>", self.validate)
        self.entry.bind("<Tab>", self.tab)

        self.bind("<Control-h>", self.toggle_hidden)
        self.bind("<Alt-Left>", self.hist_back)
        self.bind("<Alt-Right>", self.hist_forward)
        self.bind("<Alt-Up>", self.go_to_parent)
        self.bind("<Alt-Down>", self.go_to_children)
        self.bind_all("<Button-1>", self.unpost, add=True)
        self.bind_all("<FocusIn>", self.hide_listbox)

        if mode != "save":
            self.bind("<Control-l>", self.toggle_path_entry)

    def key_browse_hide(self, event):
        """ hide key browsing entry """
        if self.key_browse_entry.winfo_ismapped():
            self.key_browse_entry.place_forget()
            self.key_browse_entry.delete(0, "end")

    def key_browse_show(self, event):
        """ show key browsing entry """
        if event.char.isalnum() or event.char in [".", "_", "(", "-", "*"]:
            self.key_browse_entry.place(in_=self.right_tree, relx=0, rely=1,
                                        y=4, x=20, anchor="nw")
            self.key_browse_entry.focus_set()
            self.key_browse_entry.insert(0, event.char)

    def key_browse_validate(self, event):
        """ hide key browsing entry and validate selection """
        self.key_browse_hide(event)
        self.validate()

    def key_browse(self, *args):
        """ use keyboard to browse tree """
        self.key_browse_entry.unbind("<Up>")
        self.key_browse_entry.unbind("<Down>")
        deb = self.key_browse_entry.get()
        if deb:
            children = self.right_tree.get_children("")
            self.paths_beginning_by = [i for i in children if os.path.split(i)[-1][:len(deb)].lower() == deb]
            sel = self.right_tree.selection()
            if sel:
                self.right_tree.selection_remove(*sel)
            if self.paths_beginning_by:
                self.paths_beginning_by_index = 0
                self.browse_list(0)
                self.key_browse_entry.bind("<Up>",
                                           lambda e: self.browse_list(-1))
                self.key_browse_entry.bind("<Down>",
                                           lambda e: self.browse_list(1))

    def browse_list(self, delta):
        """ use Up and Down keys to navigate between folders/files beginning by
            the letters in self.key_browse_entry """
        self.paths_beginning_by_index += delta
        self.paths_beginning_by_index %= len(self.paths_beginning_by)
        sel = self.right_tree.selection()
        if sel:
            self.right_tree.selection_remove(*sel)
        path = os.path.abspath(os.path.join(self.history[self.hist_index],
                                            self.paths_beginning_by[self.paths_beginning_by_index]))
        self.right_tree.see(path)
        self.right_tree.selection_add(path)

    def unpost(self, event):
        """ unpost the filetype selection menu on click and hide
            self.key_browse_entry """
        if self.menu:
            w, h = self.menu.winfo_width(), self.menu.winfo_height()
            dx = event.x_root - self.menu.winfo_x()
            dy = event.y_root - self.menu.winfo_y()
            if dx < 0 or dx > w or dy < 0 or dy > h:
                self.menu.unpost()
        if event.widget != self.key_browse_entry:
            self.key_browse_hide(event)

    def hide_listbox(self, event):
        if event.widget not in [self.listbox, self.entry, self.listbox_frame]:
            self.listbox_frame.place_forget()

    # path completion in entries: key bindings
    def down(self, event):
        self.listbox.focus_set()
        self.listbox.selection_set(0)

    def tab(self, event):
        self.entry = event.widget
        self.entry.selection_clear()
        self.entry.icursor("end")
        return "break"

    def select_enter(self, event, d):
        self.entry.delete(0, "end")
        self.entry.insert(0, os.path.join(d, self.listbox.selection_get()))
        self.entry.selection_clear()
        self.entry.focus_set()
        self.entry.icursor("end")

    def select_mouse(self, event, d):
        self.entry.delete(0, "end")
        self.entry.insert(0, os.path.join(d, self.listbox.get("@%i,%i" % (event.x, event.y))))
        self.entry.selection_clear()
        self.entry.focus_set()
        self.entry.icursor("end")

    def completion(self, action, modif, pos, prev_txt):
        """ completion of the text in the path entry with existing
            folder/file names """
        if self.entry.selection_present():
            sel = self.entry.selection_get()
            txt = prev_txt.replace(sel, '')
        else:
            txt = prev_txt
        if action == "0":
            self.listbox_frame.place_forget()
            txt = txt[:int(pos)] + txt[int(pos)+1:]
        else:
            txt = txt[:int(pos)] + modif + txt[int(pos):]
            d, f = os.path.split(txt)
            if f:
                if not os.path.isabs(txt) and self.mode == "save":
                    try:
                        d2 = os.path.join(self.history[self.hist_index], d)
                        root, dirs, files = os.walk(d2).send(None)
                        files.sort(key=lambda n: n.lower())
                        extension = self.filetypes[self.filetype.get()]
                        l2 = []
                        if extension == [""]:
                            l2.extend([i for i in files if i[:len(f)] == f])
                        else:
                            for i in files:
                                ext = os.path.splitext(i)[-1]
                                if ext in extension and i[:len(f)] == f:
                                    l2.append(i)
                        l2.extend([i + "/" for i in dirs if i[:len(f)] == f])
                    except StopIteration:
                        l2 = []
                        print("error")
                else:
                    try:
                        root, dirs, files = os.walk(d).send(None)
                        dirs.sort(key=lambda n: n.lower())
                        files.sort(key=lambda n: n.lower())
                        l2 = [i + "/" for i in dirs if i[:len(f)] == f]
                        extension = self.filetypes[self.filetype.get()]
                        if extension == [""]:
                            l2.extend([i for i in files if i[:len(f)] == f])
                        else:
                            for i in files:
                                ext = os.path.splitext(i)[-1]
                                if ext in extension and i[:len(f)] == f:
                                    l2.append(i)

                    except StopIteration:
                        l2 = []
                        print("error")

                if len(l2) == 1:
                    self.listbox_frame.place_forget()
                    i = self.entry.index("insert")
                    self.entry.delete(0, "end")
                    self.entry.insert(0, os.path.join(d, l2[0]))
                    self.entry.selection_range(i+1, "end")
                    self.entry.icursor(i+1)

                elif len(l2) > 1:
                    self.listbox.bind("<Return>", lambda e, arg=d: self.select_enter(e, arg))
                    self.listbox.bind("<Button-1>", lambda e, arg=d: self.select_mouse(e, arg))
                    self.listbox_var.set(" ".join(l2))
                    self.listbox_frame.lift()
                    self.listbox.configure(height=len(l2))
                    self.listbox_frame.place(in_=self.entry, relx=0, rely=1,
                                             anchor="nw", relwidth=1)
        return True

    def toggle_path_entry(self, event):
        if self.entry.winfo_ismapped():
            self.entry.grid_remove()
            self.entry.delete(0, "end")
        else:
            self.entry.grid()
            self.entry.insert(0, self.history[self.hist_index])
            self.entry.selection_clear()
            self.entry.icursor("end")
            self.entry.focus_set()

    def go_left(self, event):
        """ move focus to left pane """
        sel = self.left_tree.selection()
        if not sel:
            sel = os.path.expanduser("~")
        else:
            sel = sel[0]
        self.left_tree.focus_set()
        self.left_tree.focus(sel)

    # go to parent/children folder with Alt+Up/Down
    def go_to_parent(self, event):
        parent = os.path.dirname(self.path_var.get())
        self.display_folder(parent, update_bar=False)

    def go_to_children(self, event):
        lb = [b.get_value() for b in self.path_bar_buttons]
        i = lb.index(self.path_var.get())
        if i < len(lb) - 1:
            self.display_folder(lb[i+1], update_bar=False)

    # navigate in history with Alt+Left/ Right keys
    def hist_back(self, event):
        if self.hist_index > -len(self.history):
            self.hist_index -= 1
            self.display_folder(self.history[self.hist_index], reset=False)

    def hist_forward(self, event):
        self.left_tree.selection_remove(*self.left_tree.selection())
        if self.hist_index < -1:
            self.hist_index += 1
            self.display_folder(self.history[self.hist_index], reset=False)

    def create_folder(self, event=None):
        """ create new folder in current location """
        def ok(event):
            name = e.get()
            e.destroy()
            if name:
                path = self.history[self.hist_index]
                folder = os.path.join(path, name)
                try:
                    os.mkdir(folder)
                except Exception:
                    pass
                self.display_folder(path)

        def cancel(event):
            e.destroy()
            self.right_tree.delete("tmp")

        self.right_tree.insert("", 0, "tmp", tags=("folder",))
        e = Entry(self)
        x, y, w, h = self.right_tree.bbox("tmp", column="#0")
        e.place(in_=self.right_tree, x=x+40, y=y,
                width=w - x - 40)
        e.bind("<Return>", ok)
        e.bind("<Escape>", cancel)
        e.bind("<FocusOut>", cancel)
        e.focus_set()

    def display_folder(self, folder, reset=True, update_bar=True):
        """ display the content of folder in self.right_tree
            - reset (boolean): forget all the part of the history right of self.hist_index
            - update_bar (boolean): update the buttons in path bar """
        folder = os.path.abspath(folder)  # remove trailing / if any
        if reset:  # reset history
            if not self.hist_index == -1:
                self.history = self.history[:self.hist_index+1]
                self.hist_index = -1
            self.history.append(folder)
        if update_bar:  # update path bar
            self.update_path_bar(folder)
        self.path_var.set(folder)
        if self.mode != "save" and self.entry.winfo_ismapped():
            self.entry.delete(0, "end")
            self.entry.insert(0, folder)
            self.entry.selection_clear()
            self.entry.icursor("end")
        self.right_tree.delete(*self.right_tree.get_children(""))  # clear self.right_tree
        try:
            root, dirs, files = os.walk(folder).send(None)
            # display folders first
            dirs.sort(key=lambda n: n.lower())
            for i, d in enumerate(dirs):
                if d[0] == ".":
                    tags = ("folder", str(i % 2), "hidden")
                else:
                    tags = ("folder", str(i % 2))
                p = os.path.join(root, d)
                self.right_tree.insert("", "end", p, text=d,
                                       values=("", get_modification_date(p)), tags=tags)
            # display files
            files.sort(key=lambda n: n.lower())
            extension = self.filetypes[self.filetype.get()]
            if extension == [""]:
                for i, f in enumerate(files):
                    if f[0] == ".":
                        tags = ("file", str(i % 2), "hidden")
                    else:
                        tags = ("file", str(i % 2))
                    p = os.path.join(root, f)
                    self.right_tree.insert("", "end", p, text=f, tags=tags,
                                           values=(get_size(p),
                                                   get_modification_date(p)))
            else:
                for i, f in enumerate(files):
                    ext = os.path.splitext(f)[-1]
                    if ext in extension:
                        if f[0] == ".":
                            tags = ("file", str(i % 2), "hidden")
                        else:
                            tags = ("file", str(i % 2))
                        p = os.path.join(root, f)
                        self.right_tree.insert("", "end", p, text=f, tags=tags,
                                               values=(get_size(p),
                                                       get_modification_date(p)))
            items = self.right_tree.get_children("")
            if items:
                self.right_tree.focus_set()
                self.right_tree.focus(items[0])
        except StopIteration:
            print("err")

    def file_selection_save(self, event):
        """ save mode only: put selected file name in name_entry """
        sel = self.right_tree.selection()
        if sel:
            sel = sel[0]
            if "file" in self.right_tree.item(sel, "tags"):
                self.entry.delete(0, "end")
                self.entry.insert(0, self.right_tree.item(sel, "text"))

    def file_selection_openfile(self, event):
        """ put selected file name in path_entry if visible """
        sel = self.right_tree.selection()
        if sel and self.entry.winfo_ismapped():
            self.entry.insert("end", self.right_tree.item(sel[0], "text"))
            self.entry.selection_clear()
            self.entry.icursor("end")

    def file_selection_opendir(self, event):
        """ prevent selection of files in opendir mode and
            put selected folder name in path_entry if visible """
        sel = self.right_tree.selection()
        if sel:
            for s in sel:
                if "file" in self.right_tree.item(s, "tags"):
                    self.right_tree.selection_remove(s)
            sel = self.right_tree.selection()
            if len(sel) == 1 and self.entry.winfo_ismapped():
                self.entry.insert("end", self.right_tree.item(sel[0], "text"))
                self.entry.selection_clear()
                self.entry.icursor("end")

    def shortcut_select(self, event):
        """ selection of a shortcut (left pane)"""
        sel = self.left_tree.selection()
        if sel:
            sel = sel[0]
            self.display_folder(sel)

    def select(self, event):
        """ display folder content on double click / Enter, validate if file """
        sel = self.right_tree.selection()
        if sel:
            sel = sel[0]
            if "folder" in self.right_tree.item(sel, "tags"):
                self.display_folder(sel)
            elif self.mode != "opendir":
                self.validate(event)
        elif self.mode == "opendir":
            self.validate(event)

    def toggle_hidden(self, event):
        """ toggle the visibility of hidden files/folders """
        if self.hide:
            self.hide = False
            for item in reversed(self.hidden):
                self.right_tree.move(item, "", 0)
            self.hidden = ()
        else:
            self.hide = True
            self.hidden = self.right_tree.tag_has("hidden")
            self.right_tree.detach(*self.right_tree.tag_has("hidden"))

    def update_path_bar(self, path):
        for b in self.path_bar_buttons:
            b.destroy()
        self.path_bar_buttons = []
        if path == "/":
            folders = [""]
        else:
            folders = path.split("/")
        b = PathButton(self.path_bar, self.path_var, "/", image=self.im_drive,
                       command=lambda: self.display_folder("/"))
        self.path_bar_buttons.append(b)
        b.grid(row=0, column=1, sticky="ns", padx=1)
        p = "/"
        for i, folder in enumerate(folders[1:]):
            p = os.path.join(p, folder)
            b = PathButton(self.path_bar, self.path_var, p, text=folder,
                           width=len(folder) + 1,
                           command=lambda f=p: self.display_folder(f),
                           style="path.TButton")
            self.path_bar_buttons.append(b)
            b.grid(row=0, column=i + 2, sticky="ns", padx=1)

    def get_result(self):
        return self.result

    def quit(self):
        self.unbind_all("<FocusIn>")
        self.unbind_all("<Button-1>")
        self.destroy()

    def validate(self, event=None):
        if self.mode == "save":
            name = self.entry.get()
            if name:
                ext = os.path.splitext(name)[-1]
                if not ext and not name[-1] == "/":
                    name += self.defaultext
                if os.path.isabs(name):
                    if os.path.exists(os.path.dirname(name)):
                        rep = True
                        if os.path.isfile(name):
                            rep = askyesnocancel(_("Confirmation"),
                                                 _("The file {file} already exists, do you want to replace it?").format(file=name),
                                                 icon="warning")
                        elif os.path.isdir(name):  # it's a directory
                            rep = False
                            self.display_folder(name)
                        path = name
                    else:  # the path is invalid
                        rep = False
                else:
                    path = os.path.join(self.history[self.hist_index], name)
                    rep = True
                    if os.path.exists(path):
                        if os.path.isfile(path):
                            rep = askyesnocancel(_("Confirmation"),
                                                 _("The file {file} already exists, do you want to replace it?").format(file=name),
                                                 icon="warning")
                        else:  # it's a directory
                            rep = False
                            self.display_folder(path)
                    elif not os.path.exists(os.path.dirname(path)):
                        # the path is invalid
                        rep = False
                if rep:
                    self.result = path
                    self.quit()
                elif rep is None:
                    self.quit()
                else:
                    self.entry.delete(0, "end")
                    self.entry.focus_set()
        else:
            name = self.entry.get()
            if name:  # get file/folder from entry
                if not os.path.exists(name):
                    self.entry.delete(0, "end")
                elif self.mode == "openfile":
                    if os.path.isfile(name):
                        self.result = name
                        self.quit()
                    else:
                        self.display_folder(name)
                else:
                    self.result = name
                    self.quit()
            # get file/folder from tree selection
            elif self.multiple_selection:
                sel = self.right_tree.selection()
                if self.mode == "opendir":
                    if sel:
                        self.result = sel
                    else:
                        self.result = (self.history[self.hist_index],)
                    self.quit()
                else:  # mode == openfile
                    if len(sel) == 1:
                        sel = sel[0]
                        if "folder" in self.right_tree.item(sel, "tags"):
                            self.display_folder(sel)
                    elif len(sel) > 1:
                        files = tuple(s for s in sel if "file" in self.right_tree.item(s, "tags"))
                        if files:
                            self.result = files
                            self.quit()
                        else:
                            self.right_tree.selection_remove(*sel)
            else:
                sel = self.right_tree.selection()
                if self.mode == "openfile":
                    if len(sel) == 1:
                        sel = sel[0]
                        if "folder" in self.right_tree.item(sel, "tags"):
                            self.display_folder(sel)
                        else:
                            self.result = sel
                            self.quit()
                else:  # mode == "opendir"
                    if len(sel) == 1:
                        self.result = sel[0]
                    else:
                        self.result = self.history[self.hist_index]
                    self.quit()


def askopendirname(parent=None, title=_("Open"), **kwargs):
    """ Return '' or the absolute path of the chosen directory.
        Options:
        - initialdir: initial folder whose content is displayed
        - initialfile: initial selected item (just the name, not the full path)
        - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
    """
    dialog = FileBrowser(parent, mode="opendir", multiple_selection=False,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()


def askopendirnames(parent=None, title=_("Open"), **kwargs):
    """ Return () or the tuple of the absolute paths of the chosen directories
        Options:
        - initialdir: initial folder whose content is displayed
        - initialfile: initial selected item (just the name, not the full path)
        - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
    """
    dialog = FileBrowser(parent, mode="opendir", multiple_selection=True,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    res = dialog.get_result()
    if not res:  # type consistency: always return a tuple
        res = ()
    return res


def askopenfilename(parent=None, title=_("Open"), **kwargs):
    """ Return '' or the absolute path of the chosen file
        Options:
        - initialdir: initial folder whose content is displayed
        - initialfile: initial selected item (just the name, not the full path)
        - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
    """
    dialog = FileBrowser(parent, mode="openfile", multiple_selection=False,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()


def askopenfilenames(parent=None, title=_("Open"), **kwargs):
    """ Return () or the tuple of the absolute paths of the chosen files
        Options:
        - initialdir: initial folder whose content is displayed
        - initialfile: initial selected item (just the name, not the full path)
        - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
    """
    dialog = FileBrowser(parent,  mode="openfile", multiple_selection=True,
                         title=title, **kwargs)
    dialog.wait_window(dialog)
    res = dialog.get_result()
    if not res:  # type consistency: always return a tuple
        res = ()
    return res


def asksaveasfilename(parent=None, title=_("Save As"), **kwargs):
    """ Return '' or the chosen absolute path (the file might not exist)
        Options:
        - initialdir: initial folder whose content is displayed
        - initialfile: initial selected item (just the name, not the full path)
        - defaultext (save mode only): extension added to filename if none is given
        - filetypes: [('name', '*.ext1|*.ext2|..'), ...]
          show only files of given filetype ("*" for all files)
    """
    dialog = FileBrowser(parent, mode="save", title=title, **kwargs)
    dialog.wait_window(dialog)
    return dialog.get_result()
