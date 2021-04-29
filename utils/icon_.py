import os
import sys

from PyQt5 import QtGui


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        base_path = sys._MEIPASS
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_logo():
    filename = resource_path(os.path.join("ico", "logo.ico"))
    icon = QtGui.QIcon()
    icon.addPixmap(QtGui.QPixmap(filename))
    return icon
