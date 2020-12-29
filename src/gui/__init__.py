#!/usr/bin/python
# -*- coding: utf-8 -*-

# IMDb Relational Dataset Generator
# Copyright (C) 2012  Jef Van den Brandt
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 2 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>

"""
Python package that holds all classes of the generated GUI elements.

Generates Python classes based on .ui files created with Qt Designer.
When doing this by hand:
pyuic4.bat entity_widget.ui > entity_widget.py

http://stackoverflow.com/questions/2489643/using-qtdesigner-with-pyqt-and-python-2-6http://stackoverflow.com/questions/119167/adding-code-to-init-py_
http://stackoverflow.com/questions/50499/in-python-how-do-i-get-the-path-and-name-of-the-file-that-is-currently-executing
http://kontrolcu.googlecode.com/svn/trunk/setup.py
"""
from PyQt4.uic import compileUiDir
import os

# the directory of this file
fdir = os.path.dirname(os.path.abspath(__file__))

os.system("{pyrcc4} -o {ofile} {qrc}".format(
        pyrcc4="pyrcc4.exe" if os.name == "nt" else "/usr/bin/pyrcc4",
        qrc=os.path.join(fdir, os.pardir, os.pardir, "icons", "icons.qrc"),
        ofile=os.path.join(fdir, "icons_rc.py")))

#mapper = lambda d, f: (d, f[:-3] + '_ui.py')
compileUiDir(fdir) #, map=mapper)

# hide package names from importer
from gui.main_window import Ui_MainWindow
from gui.entity_widget import Ui_EntityWidget

print("UI elements generated.")
