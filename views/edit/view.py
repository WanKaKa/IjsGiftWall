import os

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QDialog
from PyQt5 import QtCore

from database import database_json
from utils import path_utils, ico_utils
from views.edit import edit_gift_ui, add_gift
import giftdata
from views import dialog
from giftdata import urls

add_gift_item_list = []


class EditGiftView(QWidget, edit_gift_ui.Ui_Form):
    def __init__(self, parent=None):
        super(EditGiftView, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("广告配置编辑-为便捷而生")
        self.setWindowIcon(ico_utils.get_favicon_icon())

        pix_map = QPixmap(ico_utils.resource_path(os.path.join("ico", "logo.png")))
        self.ijoysoft_icon.setPixmap(pix_map)
        self.pushButton.clicked.connect(lambda: set_out_file(self))
        self.pushButton_2.clicked.connect(lambda: set_language(self))
        self.refresh_ui.clicked.connect(self.init_view)
        self.reload_data.clicked.connect(lambda: request_reload_data(self))
        self.add_gift_wall.clicked.connect(lambda: add_gift_wall(self))

    def init_view(self):
        if add_gift_item_list:
            self.tableWidget.setRowCount(len(add_gift_item_list))

            self.tableWidget.keyPressEvent = self.key_press_event
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.tableWidget.setColumnCount(6)
            self.tableWidget.setHorizontalHeaderLabels(['序号', '图标', '项目名', '产品名 类型', '包名', '推广图'])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setIconSize(QSize(72, 72))
            self.tableWidget.setColumnWidth(0, 80)
            self.tableWidget.setColumnWidth(1, 80)
            self.tableWidget.setColumnWidth(2, 240)
            self.tableWidget.setColumnWidth(3, 240)
            self.tableWidget.setColumnWidth(4, 360)
            self.tableWidget.setColumnWidth(5, 80)
            for i in range(len(add_gift_item_list)):
                self.tableWidget.setRowHeight(i, 80)

            for i in range(len(add_gift_item_list)):
                self.set_table_widget_item(i, add_gift_item_list[i])

    def set_table_widget_item(self, index, entity):
        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 30))
        item.setForeground(QBrush(QColor(85, 85, 255)))
        item.setText(str(index + 1))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 0, item)

        item = QTableWidgetItem()
        icon = QIcon(path_utils.get_download_path() + entity.icon_image_path)
        item.setIcon(icon)
        self.tableWidget.setItem(index, 1, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setForeground(QBrush(QColor(85, 85, 255)))
        item.setText(entity.project_name)
        self.tableWidget.setItem(index, 2, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setText("产品名: " + (entity.title if entity.title else "") +
                     "\n类   型: " + (entity.app_type if entity.app_type else ""))
        self.tableWidget.setItem(index, 3, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setText(entity.package_name)
        self.tableWidget.setItem(index, 4, item)

        item = None
        if entity.poster_path:
            item = QTableWidgetItem()
            icon = QIcon(path_utils.get_download_path() + entity.poster_path)
            item.setIcon(QIcon(icon))
        self.tableWidget.setItem(index, 5, item)

    def key_press_event(self, event):
        if event.key() == QtCore.Qt.Key_Delete:
            while self.tableWidget.selectedItems():
                row = self.tableWidget.selectedItems()[0].row()
                self.tableWidget.removeRow(row)
                add_gift_item_list.remove(add_gift_item_list[row])
            self.init_view()
        elif event.key() == QtCore.Qt.Key_Up:
            self.move_table_widget_item(True)
        elif event.key() == QtCore.Qt.Key_Down:
            self.move_table_widget_item(False)
        else:
            super().keyPressEvent(event)

    def move_table_widget_item(self, up):
        selected_rows = []
        for item in self.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        if len(selected_rows) == 1:
            row = selected_rows[0]
            new_row = max(selected_rows[0] - 1, 0) if up else min(row + 1, len(add_gift_item_list) - 1)
            entity = add_gift_item_list[row]
            add_gift_item_list.remove(entity)
            add_gift_item_list.insert(new_row, entity)
            self.set_table_widget_item(row, add_gift_item_list[row])
            self.set_table_widget_item(new_row, add_gift_item_list[new_row])
            self.tableWidget.selectRow(new_row)


class AddGiftView(QDialog, add_gift.Ui_Dialog):
    def __init__(self, parent=None):
        super(AddGiftView, self).__init__(parent)
        self.setupUi(self)

        self.item_list = None
        self.setWindowTitle("添加GiftWall-为便捷而生")
        self.setWindowIcon(ico_utils.get_favicon_icon())
        self.init_view()

    def init_view(self):
        self.item_list = giftdata.overall_gift_entity.item_list if giftdata.overall_gift_entity else None
        if self.item_list:
            self.tableWidget.setRowCount(len(self.item_list))

            self.tableWidget.keyPressEvent = self.key_press_event
            self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
            self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(['序号', '图标', '项目名', '产品名 类型', '包名', '推广图', "添加状态"])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setIconSize(QSize(36, 36))
            self.tableWidget.setColumnWidth(0, 60)
            self.tableWidget.setColumnWidth(1, 60)
            self.tableWidget.setColumnWidth(2, 200)
            self.tableWidget.setColumnWidth(3, 200)
            self.tableWidget.setColumnWidth(4, 320)
            self.tableWidget.setColumnWidth(5, 60)
            self.tableWidget.setColumnWidth(6, 120)
            for i in range(len(self.item_list)):
                self.tableWidget.setRowHeight(i, 40)

            for i in range(len(self.item_list)):
                self.set_table_widget_item(i, self.item_list[i])

    def set_table_widget_item(self, index, entity):
        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 20))
        item.setForeground(QBrush(QColor(85, 85, 255)))
        item.setText(str(index + 1))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 0, item)

        item = QTableWidgetItem()
        icon = QIcon(path_utils.get_download_path() + entity.icon_image_path)
        item.setIcon(icon)
        self.tableWidget.setItem(index, 1, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setForeground(QBrush(QColor(85, 85, 255)))
        item.setText(entity.project_name)
        self.tableWidget.setItem(index, 2, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setText("产品名: " + (entity.title if entity.title else "") +
                     "\n类   型: " + (entity.app_type if entity.app_type else ""))
        self.tableWidget.setItem(index, 3, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setText(entity.package_name)
        self.tableWidget.setItem(index, 4, item)

        item = None
        if entity.poster_path:
            item = QTableWidgetItem()
            icon = QIcon(path_utils.get_download_path() + entity.poster_path)
            item.setIcon(QIcon(icon))
        self.tableWidget.setItem(index, 5, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 16))
        item.setForeground(QBrush(QColor(255, 0, 0)))
        item.setText("已添加")
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 6, item)

    def key_press_event(self, event):
        pass


def set_out_file(edit_gift_view):
    out_file_dialog = dialog.SelectDialog(edit_gift_view)
    out_file_dialog.show()
    out_file_dialog.setWindowTitle("选择文件名-为便捷而生")
    out_file_dialog.setWindowIcon(ico_utils.get_favicon_icon())

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
        out_file_radio_button_list[i].setChecked(edit_gift_view.file_name.text() == urls.XML_NAME_LIST[i])
        out_file_radio_button_list[i].toggled.connect(
            lambda: get_out_file(edit_gift_view, out_file_dialog, out_file_radio_button_list))
    # 隐藏多出来的按钮
    if len(out_file_radio_button_list) > len(urls.XML_NAME_LIST):
        for i in range(len(out_file_radio_button_list)):
            if i >= len(urls.XML_NAME_LIST):
                out_file_radio_button_list[i].hide()
    out_file_dialog.exec()


def get_out_file(edit_gift_view, out_file_dialog, out_file_radio_button_list):
    if out_file_radio_button_list:
        for radio_button in out_file_radio_button_list:
            if radio_button.isChecked():
                edit_gift_view.file_name.setText(radio_button.text())
                out_file_dialog.hide()


def set_language(edit_gift_view):
    language_dialog = dialog.MultipleSelectDialog(edit_gift_view)
    language_dialog.show()
    language_dialog.setWindowTitle("选择地区-为便捷而生")
    language_dialog.setWindowIcon(ico_utils.get_favicon_icon())

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
        language_dialog.checkBox_15,
        language_dialog.checkBox_16,
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setText(_translate("Dialog", urls.LANGUAGE_LIST[i].ljust(50, " ")))
        language_check_box_list[i].setChecked(urls.LANGUAGE_LIST[i] in edit_gift_view.language.text())
        language_check_box_list[i].toggled.connect(
            lambda: get_language(edit_gift_view, language_check_box_list))
    # 隐藏多出来的按钮
    if len(language_check_box_list) > len(urls.LANGUAGE_LIST):
        for i in range(len(language_check_box_list)):
            if i >= len(urls.LANGUAGE_LIST):
                language_check_box_list[i].hide()
    language_dialog.deselect_all.clicked.connect(lambda: select_all_language(language_check_box_list, False))
    language_dialog.select_all.clicked.connect(lambda: select_all_language(language_check_box_list, True))
    language_dialog.exec()


def get_language(edit_gift_view, language_check_box_list):
    if language_check_box_list:
        edit_gift_view.language.setText("")
        for radio_button in language_check_box_list:
            if radio_button.isChecked():
                edit_gift_view.language.setText(edit_gift_view.language.text() + radio_button.text().strip(" ") + ",")


def select_all_language(language_check_box_list, enable):
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setChecked(enable)


def request_reload_data(edit_gift_view):
    reply = QMessageBox.question(edit_gift_view, '重新下载', '确认重新下载服务器数据吗?', QMessageBox.No | QMessageBox.Yes,
                                 QMessageBox.No)
    if reply == QMessageBox.Yes:
        database_json.save(database_json.KEY_GIFT_DATA_UPDATE_TIME, 0)
        database_json.save(database_json.KEY_GIFT_ICON_UPDATE_TIME, 0)
        giftdata.download.load_config()


def add_gift_wall(edit_gift_view):
    add_gift_view = AddGiftView(edit_gift_view)
    add_gift_view.show()
    # add_gift_view.setWindowTitle("添加GiftWall-为便捷而生")
    # add_gift_view.setWindowIcon(ico_utils.get_favicon_icon())
