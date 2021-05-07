import os

from PyQt5.QtWidgets import QMessageBox

from PyQt5.QtWidgets import QWidget
import gui.main.operation.check_ui
from util import path_


class CheckMenu(QWidget, gui.main.operation.check_ui.Ui_Form):
    def __init__(self, parent=None):
        super(CheckMenu, self).__init__(None)
        self.setupUi(self)

        self.open_outputs_2.clicked.connect(lambda: os.system("start " + path_.get_outputs()))
        self.clear_outputs_2.clicked.connect(parent.delete_dir)

        self.save.clicked.connect(parent.fun_create_gift_wall_file)
        self.add_gift_wall_2.clicked.connect(parent.click_add_gift_wall)
        self.cancel_save.clicked.connect(lambda: click_cancel_save(parent))


def click_cancel_save(view_):
    reply = QMessageBox.question(
        view_, '放弃修改', '确定放弃修改吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
    if reply == QMessageBox.Yes:
        view_.load_outputs_xml_file()
