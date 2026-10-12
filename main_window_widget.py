import os

from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtWidgets import QWidget, QLayout

from app.app_update.app_update_widget import QKevinAppUpdate
from app.edit_gift.gui.edit_gift_widget import QEditGiftWidget
from settings_dialog import QSettingsDialog
from util import icon, ui_scale

import app.edit_gift.core.download
import main_window_ui


def set_menu_item_enable(enable, menu_layout, menu_title):
    if enable:
        menu_layout.setStyleSheet(
            "background-color: rgb(57, 61, 255); border: none; border-radius: 10px;")
        menu_title.setStyleSheet("color: rgb(255, 255, 255);\n""font: 8pt \"微软雅黑\";")
    else:
        menu_layout.setStyleSheet(
            "background-color: rgb(247, 247, 247); border: none; border-radius: 10px;")
        menu_title.setStyleSheet("color: rgb(0, 0, 0);\n""font: 8pt \"微软雅黑\";")


class QKevinMainWindow(QWidget):
    STATE_MAIN_MENU = 0
    STATE_EDIT_GIFT = 1
    STATE_APP_UPDATE = 2

    def __init__(self, parent=None):
        super(QKevinMainWindow, self).__init__(parent)
        self.ui = main_window_ui.Ui_Form()
        self.ui.setupUi(self)
        self._menu_index = 0
        self._ensure_maximized_once = False
        # QFormLayout 默认约束在子控件缩放后会把最大化宽度锁在设计稿宽度
        if self.layout() is not None:
            self.layout().setSizeConstraint(QLayout.SetNoConstraint)

        self.setWindowTitle("爱卓软工具")
        self.setWindowIcon(icon.get_logo())

        icon_size = self.ui.menu_icon_1.size()
        self.icon_edit_gift_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "edit_gift_black.png")),
            icon_size, widget=self)
        self.icon_edit_gift_white = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "edit_gift_white.png")),
            icon_size, widget=self)
        self.icon_app_update_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "app_update_black.png")),
            icon_size, widget=self)
        self.icon_app_update_white = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "app_update_white.png")),
            icon_size, widget=self)
        self.icon_settings_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "settings_black.png")),
            icon_size, widget=self)

        # 设置公司Logo（按 DPR 缩放，避免放大比例后发糊）
        ui_scale.set_label_pixmap(
            self.ui.icon, icon.resource_path(os.path.join("ico", "ijs_icon.png")))
        self.ui.menu_icon_1.setScaledContents(False)
        self.ui.menu_icon_2.setScaledContents(False)
        self.ui.menu_icon_settings.setScaledContents(False)
        self.ui.menu_icon_settings.setPixmap(self.icon_settings_black)

        self.ui.menu_layout_1.mousePressEvent = self.do_show_edit_gift
        self.ui.menu_layout_2.mousePressEvent = self.do_show_app_update
        self.ui.menu_layout_settings.mousePressEvent = self.do_show_settings
        self.ui.menu_layout_settings.setCursor(Qt.PointingHandCursor)

        # 广告配置界面
        self.edit_gift_widget = QEditGiftWidget(parent=self)
        app.edit_gift.core.download.init_gift_data(self.edit_gift_widget)
        self.edit_gift_widget.init_view()
        self.ui.verticalLayout.addWidget(self.edit_gift_widget)

        # App升级配置
        self.app_update = QKevinAppUpdate(parent=self)
        self.ui.verticalLayout.addWidget(self.app_update)

        self._settings_dialog = None
        self.show_edit_gift()
        self._relayout_settings_button()

    def select_menu(self, index):
        self._menu_index = index
        if index == 0:
            set_menu_item_enable(True, self.ui.menu_layout_1, self.ui.menu_title_1)
            set_menu_item_enable(False, self.ui.menu_layout_2, self.ui.menu_title_2)
            # 选中白、未选中黑
            self.ui.menu_icon_1.setPixmap(self.icon_edit_gift_white)
            self.ui.menu_icon_2.setPixmap(self.icon_app_update_black)
        elif index == 1:
            set_menu_item_enable(False, self.ui.menu_layout_1, self.ui.menu_title_1)
            set_menu_item_enable(True, self.ui.menu_layout_2, self.ui.menu_title_2)
            self.ui.menu_icon_1.setPixmap(self.icon_edit_gift_black)
            self.ui.menu_icon_2.setPixmap(self.icon_app_update_white)

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

    def do_show_settings(self, event):
        if self._settings_dialog is None:
            self._settings_dialog = QSettingsDialog(parent=self)
        self._settings_dialog.exec_()

    def _relayout_settings_button(self):
        """将设置按钮固定在左侧栏底部。"""
        frame = self.ui.frame
        btn = self.ui.menu_layout_settings
        margin = 8
        y = max(margin, frame.height() - btn.height() - margin)
        btn.move(btn.x(), y)

    def resizeEvent(self, event):
        super(QKevinMainWindow, self).resizeEvent(event)
        self._relayout_settings_button()

    def showEvent(self, event):
        super(QKevinMainWindow, self).showEvent(event)
        self._relayout_settings_button()
        if not self._ensure_maximized_once:
            self._ensure_maximized_once = True
            # 首帧显示后再最大化，避免缩放流程冲掉窗口状态
            QTimer.singleShot(0, self._force_maximized)

    def _force_maximized(self):
        if self.layout() is not None:
            self.layout().setSizeConstraint(QLayout.SetNoConstraint)
        self.setMinimumSize(0, 0)
        self.setMaximumSize(16777215, 16777215)
        self.setWindowState(self.windowState() | Qt.WindowMaximized)
        self.showMaximized()
        self._relayout_settings_button()

    def refresh_after_ui_scale(self):
        """显示比例变更后刷新依赖像素尺寸的图标。"""
        icon_size = self.ui.menu_icon_1.size()
        self.icon_edit_gift_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "edit_gift_black.png")),
            icon_size, widget=self)
        self.icon_edit_gift_white = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "edit_gift_white.png")),
            icon_size, widget=self)
        self.icon_app_update_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "app_update_black.png")),
            icon_size, widget=self)
        self.icon_app_update_white = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "app_update_white.png")),
            icon_size, widget=self)
        self.icon_settings_black = ui_scale.scaled_pixmap(
            icon.resource_path(os.path.join("ico", "settings_black.png")),
            icon_size, widget=self)
        ui_scale.set_label_pixmap(
            self.ui.icon, icon.resource_path(os.path.join("ico", "ijs_icon.png")))
        self.ui.menu_icon_settings.setPixmap(self.icon_settings_black)
        # 按菜单下标恢复图标（勿用 isVisible：父窗口未 show 时会误判）
        self.select_menu(self._menu_index)
        self._relayout_settings_button()
        if hasattr(self.edit_gift_widget, "refresh_after_ui_scale"):
            self.edit_gift_widget.refresh_after_ui_scale()
