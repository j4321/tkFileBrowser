# -*- coding: utf-8 -*-

from tkfilebrowser.recent_files import RecentFiles
import unittest
import tempfile
import os


class TestRecentFiles(unittest.TestCase):
    def test_recentfiles(self):
        filename = tempfile.mktemp()
        rf = RecentFiles(filename, 2)
        self.assertEqual(rf.get(), [])

        rf.add('test')
        self.assertEqual(rf.get(), ['test'])
        rf.add('test2')
        self.assertEqual(rf.get(), ['test2', 'test'])
        rf.add('test')
        self.assertEqual(rf.get(), ['test', 'test2'])
        rf.add('test3')
        self.assertEqual(rf.get(), ['test3', 'test'])

        with open(filename) as f:
            self.assertEqual(f.read().split(), rf.get())

        del rf
        rf = RecentFiles(filename, 2)
        self.assertEqual(rf.get(), ['test3', 'test'])

        os.remove(filename)
