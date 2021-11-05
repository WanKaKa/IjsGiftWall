from PyQt5 import QtCore
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import gift.download
from gui.main.app_update.app_update_widget import QKevinAppUpdate
from gui.main.edit_gift_widget import QEditGiftWidget
from gui.main.main_menu_widget import QKevinMainMenu
from util import icon

import gui.main.main_window_ui


class QKevinMainWindow(QWidget):
    STATE_MAIN_MENU = 0
    STATE_EDIT_GIFT = 1
    STATE_APP_UPDATE = 2

    def __init__(self, parent=None):
        super(QKevinMainWindow, self).__init__(parent)
        self.ui = gui.main.main_window_ui.Ui_From()
        self.ui.setupUi(self)

        self.setWindowTitle("爱卓软工具")
        self.setWindowIcon(icon.get_logo())
        self.setWindowState(Qt.WindowMaximized)
        self.keyPressEvent = self.key_press_event

        # 主菜单界面
        self.main_menu = QKevinMainMenu(parent=self)
        self.main_menu.show_edit_gift = self.show_edit_gift
        self.main_menu.show_app_update = self.show_app_update
        self.ui.verticalLayout.addWidget(self.main_menu)

        # 广告配置界面
        self.edit_gift_widget = QEditGiftWidget(parent=self)
        gift.download.init_gift_data(self.edit_gift_widget)
        self.edit_gift_widget.init_view()
        self.ui.verticalLayout.addWidget(self.edit_gift_widget)

        # App升级配置
        self.app_update = QKevinAppUpdate(parent=self)
        self.ui.verticalLayout.addWidget(self.app_update)

        self.state = None
        self.show_main_menu()

    def show_main_menu(self):
        if self.state == self.STATE_MAIN_MENU:
            return
        self.state = self.STATE_MAIN_MENU
        self.edit_gift_widget.setVisible(True)
        self.app_update.setVisible(False)

    def show_edit_gift(self):
        self.state = self.STATE_EDIT_GIFT
        self.app_update.setVisible(False)
        self.edit_gift_widget.setVisible(True)

    def show_app_update(self):
        self.state = self.STATE_APP_UPDATE
        self.edit_gift_widget.setVisible(False)
        self.app_update.setVisible(True)

    def key_press_event(self, event):
        if event.key() == Qt.Key_Escape:
            self.show_main_menu()
        else:
            super().keyPressEvent(event)
