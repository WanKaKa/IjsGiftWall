import os

from PyQt5.QtWidgets import QWidget, QMessageBox, QFileDialog

import gui.main.operation.edit_ui
from database import json_
from gift import download
from util import path_


class EditMenu(QWidget, gui.main.operation.edit_ui.Ui_Form):
    def __init__(self, parent=None):
        super(EditMenu, self).__init__(None)
        self.setupUi(self)

        self.reload_data_config.clicked.connect(lambda: click_reload_data_config(parent))
        self.reload_data.clicked.connect(lambda: click_reload_data(parent))
        self.reset_ui.clicked.connect(parent.click_reset_ui)

        self.add_gift_wall.clicked.connect(parent.click_add_gift_wall)
        self.import_gift_wall.clicked.connect(lambda: click_import_gift_wall(parent))
        self.create_gift_wall_file.clicked.connect(parent.click_create_gift_wall_file)

        self.open_outputs.clicked.connect(lambda: os.system("start " + path_.get_outputs()))
        self.clear_outputs.clicked.connect(parent.delete_dir)


def click_reload_data_config(view_):
    reply = QMessageBox.question(
        view_, '重新下载', '确认重新下载服务器配置表吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        json_.put_config_download_time(0)
        download.init_gift_data(view_)


def click_reload_data(view_):
    reply = QMessageBox.question(
        view_, '重新下载', '确认重新下载服务器数据吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        json_.put_config_download_time(0)
        json_.put_icon_download_time(0)
        download.init_gift_data(view_)


def click_import_gift_wall(view_):
    file_name, file_type = QFileDialog.getOpenFileName(view_, "选取文件", path_.get_outputs())
    view_.load_signal_xml_file(file_name)
