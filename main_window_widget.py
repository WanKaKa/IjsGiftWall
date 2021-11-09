import os

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QWidget

from app.app_update.app_update_widget import QKevinAppUpdate
from app.edit_gift.gui.edit_gift_widget import QEditGiftWidget
from util import icon

import app.edit_gift.core.download
import main_window_ui


def set_menu_item_enable(enable, menu_layout, menu_title):
    if enable:
        menu_layout.setStyleSheet("background-color: rgb(247, 247, 247);")
        menu_title.setStyleSheet("color: rgb(0, 0, 0);\n""font: 8pt \"微软雅黑\";")
    else:
        menu_layout.setStyleSheet("background-color: rgb(57, 61, 255);")
        menu_title.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"微软雅黑\";")


class QKevinMainWindow(QWidget):
    STATE_MAIN_MENU = 0
    STATE_EDIT_GIFT = 1
    STATE_APP_UPDATE = 2

    def __init__(self, parent=None):
        super(QKevinMainWindow, self).__init__(parent)
        self.ui = main_window_ui.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowTitle("爱卓软工具")
        self.setWindowIcon(icon.get_logo())
        self.setWindowState(Qt.WindowMaximized)

        self.icon_edit_gift_black = QPixmap(icon.resource_path(os.path.join("ico", "edit_gift_black.png")))
        self.icon_edit_gift_white = QPixmap(icon.resource_path(os.path.join("ico", "edit_gift_white.png")))
        self.icon_app_update_black = QPixmap(icon.resource_path(os.path.join("ico", "app_update_black.png")))
        self.icon_app_update_white = QPixmap(icon.resource_path(os.path.join("ico", "app_update_white.png")))

        # 设置公司Logo
        self.ui.icon.setPixmap(QPixmap(icon.resource_path(os.path.join("ico", "ijs_icon.png"))))

        self.ui.menu_layout_1.mousePressEvent = self.do_show_edit_gift
        self.ui.menu_layout_2.mousePressEvent = self.do_show_app_update

        # 广告配置界面
        self.edit_gift_widget = QEditGiftWidget(parent=self)
        app.edit_gift.core.download.init_gift_data(self.edit_gift_widget)
        self.edit_gift_widget.init_view()
        self.ui.verticalLayout.addWidget(self.edit_gift_widget)

        # App升级配置
        self.app_update = QKevinAppUpdate(parent=self)
        self.ui.verticalLayout.addWidget(self.app_update)

        self.show_edit_gift()

    def select_menu(self, index):
        if index == 0:
            set_menu_item_enable(True, self.ui.menu_layout_1, self.ui.menu_title_1)
            set_menu_item_enable(False, self.ui.menu_layout_2, self.ui.menu_title_2)
            self.ui.menu_icon_1.setPixmap(self.icon_edit_gift_black)
            self.ui.menu_icon_2.setPixmap(self.icon_app_update_white)
        elif index == 1:
            set_menu_item_enable(False, self.ui.menu_layout_1, self.ui.menu_title_1)
            set_menu_item_enable(True, self.ui.menu_layout_2, self.ui.menu_title_2)
            self.ui.menu_icon_1.setPixmap(self.icon_edit_gift_white)
            self.ui.menu_icon_2.setPixmap(self.icon_app_update_black)

    def show_edit_gift(self):
        self.select_menu(0)
        self.app_update.setVisible(False)
        self.edit_gift_widget.setVisible(True)

    def show_app_update(self):
        self.select_menu(1)
        self.edit_gift_widget.setVisible(False)
        self.app_update.setVisible(True)

    def do_show_edit_gift(self, event):
        self.show_edit_gift()

    def do_show_app_update(self, event):
        self.show_app_update()
