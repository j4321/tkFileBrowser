#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from setuptools import setup

from codecs import open
from os import path

here = path.abspath(path.dirname(__file__))

with open(path.join(here, 'README.rst'), encoding='utf-8') as f:
    long_description = f.read()

setup(name='tkFileBrowser',
      version='1.0.0',
      description='File browser for Tkinter, alternative to tkinter.filedialog in linux with GTK bookmarks support.',
      long_description=long_description,
      url='https://pypi.python.org/pypi/tkFileBrowser',
      author='Juliette Monsel',
      author_email='j_4321@protonmail.com',
      license='GPLv3',
      classifiers=[
            'Development Status :: 5 - Production/Stable',
            'Intended Audience :: Developers',
            'Topic :: Software Development :: Widget Sets',
            'Topic :: Software Development :: Libraries :: Python Modules',
            'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
            'Programming Language :: Python :: 3',
            'Programming Language :: Python :: 3.4',
            'Programming Language :: Python :: 3.5',
            'Programming Language :: Python :: 3.6',
            'Natural Language :: English',
            'Natural Language :: French',
            'Operating System :: POSIX :: Linux',
      ],
      keywords=['tkinter', 'filedialog', 'filebrowser'],
      py_modules=["tkFileBrowser"],
      packages = ["tkFileBrowser"],
	  package_data = {"tkFileBrowser" : ["images/*"]},
	  requires = ["os", "locale", "time", "psutil", "tkinter", "math", "urllib"]
)
