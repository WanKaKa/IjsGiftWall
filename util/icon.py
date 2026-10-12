import os
import sys

from PyQt5 import QtGui


def resource_path(relative_path):
    if getattr(sys, 'frozen', False):
        # onedir / onefile 均由 PyInstaller 设置 _MEIPASS
        base_path = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
    else:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


def get_logo():
    filename = resource_path(os.path.join("ico", "logo.ico"))
    icon_ = QtGui.QIcon()
    icon_.addPixmap(QtGui.QPixmap(filename))
    return icon_
