from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import gui.main.main_menu_ui


class QKevinMainMenu(QWidget):
    THEME_STYLE = "font: 16pt \"微软雅黑\";\ncolor: rgb(255, 255, 255);\nbackground-color: rgb(57, 61, 255);"
    NORMAL_STYLE = "font: 16pt \"微软雅黑\";\ncolor: rgb(0, 0, 0);\nbackground-color: rgb(255, 255, 255);"

    def __init__(self, parent=None):
        super(QKevinMainMenu, self).__init__(parent)
        self.ui = gui.main.main_menu_ui.Ui_Form()
        self.ui.setupUi(self)

        self.ui.pb_edit_gift.setStyleSheet(self.THEME_STYLE)
        self.ui.pb_app_update.setStyleSheet(self.NORMAL_STYLE)

        self.ui.pb_edit_gift.clicked.connect(self.do_show_edit_gift)
        self.ui.pb_app_update.clicked.connect(self.do_show_app_update)

    def do_show_edit_gift(self):
        self.ui.pb_edit_gift.setStyleSheet(self.THEME_STYLE)
        self.ui.pb_app_update.setStyleSheet(self.NORMAL_STYLE)
        self.show_edit_gift()

    def show_edit_gift(self):
        pass

    def do_show_app_update(self):
        self.ui.pb_edit_gift.setStyleSheet(self.NORMAL_STYLE)
        self.ui.pb_app_update.setStyleSheet(self.THEME_STYLE)
        self.show_app_update()

    def show_app_update(self):
        pass
