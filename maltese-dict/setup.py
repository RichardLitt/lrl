"""
This is a setup.py script generated by py2applet

Usage:
    python setup.py py2app
"""

from setuptools import setup

APP = ['Kelma.py']
DATA_FILES = ['Basic Dictionary.xml']
OPTIONS = {'arch': 'x86_64',
 'argv_emulation': True,
 'iconfile': '/Users/richardlittauer/Github/lrl/Maltese/Pages.icns'}

setup(
    app=APP,
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
)
