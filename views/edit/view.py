from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem
from PyQt5 import QtCore

from utils import path_utils
from views.edit import edit_gift_ui
import giftdata
from views import dialog
from giftdata import urls


class View(QWidget, edit_gift_ui.Ui_Form):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setupUi(self)

        self.pushButton.clicked.connect(lambda: set_out_file(self))
        self.pushButton_2.clicked.connect(lambda: set_language(self))

    def init_view(self):
        item_list = giftdata.overall_gift_entity.item_list if giftdata.overall_gift_entity else None
        if item_list:
            self.tableWidget.setRowCount(len(item_list))
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(['Icon', '项目名', '产品名', '类型', '包名', '推广图', '操作'])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setIconSize(QSize(64, 64))
            self.tableWidget.setColumnWidth(0, 80)
            self.tableWidget.setColumnWidth(1, 240)
            self.tableWidget.setColumnWidth(2, 150)
            self.tableWidget.setColumnWidth(3, 160)
            self.tableWidget.setColumnWidth(4, 360)
            self.tableWidget.setColumnWidth(5, 80)
            self.tableWidget.setColumnWidth(6, 80)
            for i in range(len(item_list)):
                self.tableWidget.setRowHeight(i, 80)

            for i in range(len(item_list)):
                item = QTableWidgetItem()
                icon = QIcon(path_utils.get_download_path() + item_list[i].icon_image_path)
                item.setIcon(QIcon(icon))
                self.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 12))
                item.setForeground(QBrush(QColor(85, 85, 255)))
                item.setText(item_list[i].project_name)
                self.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 10))
                item.setText(item_list[i].title)
                self.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 10))
                item.setText(item_list[i].app_type)
                self.tableWidget.setItem(i, 3, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 10))
                item.setText(item_list[i].package_name)
                self.tableWidget.setItem(i, 4, item)

                if item_list[i].poster_path:
                    item = QTableWidgetItem()
                    icon = QIcon(path_utils.get_download_path() + item_list[i].poster_path)
                    item.setIcon(QIcon(icon))
                    self.tableWidget.setItem(i, 5, item)


def set_out_file(edit_gift):
    out_file_dialog = dialog.SelectDialog(edit_gift)
    out_file_dialog.show()
    out_file_dialog.setWindowTitle("选择文件名-为便捷而生")
    out_file_dialog.setWindowIcon(QIcon('../favicon.ico'))

    out_file_radio_button_list = [
        out_file_dialog.radioButton,
        out_file_dialog.radioButton_2,
        out_file_dialog.radioButton_3,
        out_file_dialog.radioButton_4,
        out_file_dialog.radioButton_5,
        out_file_dialog.radioButton_6,
        out_file_dialog.radioButton_7,
        out_file_dialog.radioButton_8,
        out_file_dialog.radioButton_9,
        out_file_dialog.radioButton_10,
        out_file_dialog.radioButton_11,
        out_file_dialog.radioButton_12,
        out_file_dialog.radioButton_13,
        out_file_dialog.radioButton_14,
        out_file_dialog.radioButton_15,
        out_file_dialog.radioButton_16
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(urls.XML_NAME_LIST)):
        out_file_radio_button_list[i].setText(_translate("Form", urls.XML_NAME_LIST[i]))
        out_file_radio_button_list[i].toggled.connect(
            lambda: get_out_file(edit_gift, out_file_dialog, out_file_radio_button_list))
        out_file_radio_button_list[i].setChecked(edit_gift.label_11.text() == urls.XML_NAME_LIST[i])
    # 隐藏多出来的按钮
    if len(out_file_radio_button_list) > len(urls.XML_NAME_LIST):
        for i in range(len(out_file_radio_button_list)):
            if i >= len(urls.XML_NAME_LIST):
                out_file_radio_button_list[i].hide()
    out_file_dialog.exec()


def get_out_file(edit_gift, out_file_dialog, out_file_radio_button_list):
    if out_file_radio_button_list:
        for radio_button in out_file_radio_button_list:
            if radio_button.isChecked():
                edit_gift.label_11.setText(radio_button.text())
                out_file_dialog.hide()


def set_language(edit_gift):
    language_dialog = dialog.MultipleSelectDialog(edit_gift)
    language_dialog.show()
    language_dialog.setWindowTitle("选择地区-为便捷而生")
    language_dialog.setWindowIcon(QIcon('../favicon.ico'))

    language_check_box_list = [
        language_dialog.checkBox,
        language_dialog.checkBox_2,
        language_dialog.checkBox_3,
        language_dialog.checkBox_4,
        language_dialog.checkBox_5,
        language_dialog.checkBox_6,
        language_dialog.checkBox_7,
        language_dialog.checkBox_8,
        language_dialog.checkBox_9,
        language_dialog.checkBox_10,
        language_dialog.checkBox_11,
        language_dialog.checkBox_12,
        language_dialog.checkBox_13,
        language_dialog.checkBox_14,
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setText(_translate("Dialog", urls.LANGUAGE_LIST[i].ljust(50, " ")))
        # language_check_box_list[i].toggled.connect(
        #     lambda: get_out_file(edit_gift, language_dialog, language_check_box_list))
        # language_check_box_list[i].setChecked(edit_gift.label_11.text() == urls.LANGUAGE_LIST[i])
    # 隐藏多出来的按钮
    if len(language_check_box_list) > len(urls.LANGUAGE_LIST):
        for i in range(len(language_check_box_list)):
            if i >= len(urls.LANGUAGE_LIST):
                language_check_box_list[i].hide()
    language_dialog.exec()
