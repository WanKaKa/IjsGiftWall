from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QDialog
from PyQt5 import QtCore

from utils import path_utils
from views.edit import add_gift, edit_gift_window
import giftdata
from giftdata import urls


class AddGiftView(QDialog, add_gift.Ui_Dialog):
    OVERALL_GIFT_WALL_FILE_NAME = "总表"
    select_language = urls.LANGUAGE_LIST[0]
    select_gift_name = OVERALL_GIFT_WALL_FILE_NAME

    def __init__(self, parent=None):
        super(AddGiftView, self).__init__(parent)
        self.setupUi(self)

        self.server_gift_wall_file = [self.OVERALL_GIFT_WALL_FILE_NAME]
        for file in urls.XML_NAME_LIST:
            self.server_gift_wall_file.append(file)
        self.item_list = []

        self.language_radio_list = [
            self.language_radio_1,
            self.language_radio_2,
            self.language_radio_3,
            self.language_radio_4,
            self.language_radio_5,
            self.language_radio_6,
            self.language_radio_7,
            self.language_radio_8,
            self.language_radio_9,
            self.language_radio_10,
            self.language_radio_11,
            self.language_radio_12,
        ]
        self.file_name_radio_list = [
            self.file_name_radio_1,
            self.file_name_radio_2,
            self.file_name_radio_3,
            self.file_name_radio_4,
            self.file_name_radio_5,
            self.file_name_radio_6,
            self.file_name_radio_7,
            self.file_name_radio_8,
            self.file_name_radio_9,
            self.file_name_radio_10,
            self.file_name_radio_11,
            self.file_name_radio_12,
        ]
        self.init_view()

        self.tableWidget.keyPressEvent = self.key_press_event
        self.tableWidget.itemClicked.connect(self.click_table_item)
        self.tableWidget.itemDoubleClicked.connect(self.click_table_item_double)
        self.add.clicked.connect(self.click_add_gift_wall)

    def init_view(self):
        self.init_radio_button(0, self.language_radio_list, urls.LANGUAGE_LIST)
        self.init_radio_button(1, self.file_name_radio_list, self.server_gift_wall_file)

        self.init_table_widget()
        self.set_table_widget()

    def init_radio_button(self, type_value, radio_list, string_list):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(string_list)):
            radio_list[i].setText(_translate("Form", string_list[i]))
            if type_value == 0:
                if self.select_language == radio_list[i].text():
                    radio_list[i].setChecked(True)
            else:
                if self.select_gift_name == radio_list[i].text():
                    radio_list[i].setChecked(True)
            radio_list[i].toggled.connect(
                lambda: click_edit_view_radio_button(self, type_value, radio_list))
        # 隐藏多出来的按钮
        if len(radio_list) > len(string_list):
            for i in range(len(radio_list)):
                if i >= len(string_list):
                    radio_list[i].hide()

    def init_table_widget(self):
        self.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.tableWidget.setColumnCount(7)
        self.tableWidget.setHorizontalHeaderLabels(['序号', '图标', '项目名', '产品名 类型', '包名', '推广图', "添加状态"])
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setIconSize(QSize(36, 36))
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 240)
        self.tableWidget.setColumnWidth(3, 270)
        self.tableWidget.setColumnWidth(4, 320)
        self.tableWidget.setColumnWidth(5, 60)
        self.tableWidget.setColumnWidth(6, 120)

    def set_table_widget(self):
        if self.item_list:
            self.item_list.clear()
        if giftdata.overall_gift_entity and giftdata.overall_gift_entity.item_list:
            if self.OVERALL_GIFT_WALL_FILE_NAME == self.select_gift_name:
                self.item_list = giftdata.overall_gift_entity.item_list[:]
            else:
                if self.select_gift_name in giftdata.gift_entity_list[self.select_language]:
                    gift_entity = giftdata.gift_entity_list[self.select_language][self.select_gift_name]
                    if gift_entity and gift_entity.item_list:
                        for item1 in gift_entity.item_list:
                            for item2 in giftdata.overall_gift_entity.item_list:
                                if edit_gift_window.compare_entity(item1, item2):
                                    self.item_list.append(item2)
                                    break
        if self.item_list:
            self.tableWidget.setRowCount(len(self.item_list))
            for i in range(len(self.item_list)):
                self.set_table_widget_item(i, self.item_list[i])
        else:
            self.tableWidget.setRowCount(0)

    def set_table_widget_item(self, index, entity):
        self.tableWidget.setRowHeight(index, 40)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 18))
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

        self.set_table_widget_item_state(index, edit_gift_window.is_entity_added(entity))

    def set_table_widget_item_state(self, index, state):
        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setForeground(QBrush(QColor(255, 0, 0)))
        item.setText("已添加" if state else "")
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 6, item)

    def click_table_item(self):
        print(self.tableWidget.currentItem().text())

    def click_table_item_double(self):
        row = self.tableWidget.currentItem().row()
        if 0 <= row < len(self.item_list):
            self.add_gift_item(row)

    def key_press_event(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            self.tableWidget.selectAll()
        elif event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_D:
            selected_rows = []
            for item in self.tableWidget.selectedItems():
                if item.row() not in selected_rows:
                    selected_rows.append(item.row())
            for row in selected_rows:
                if self.tableWidget.item(row, 6).text():
                    delete_entity = None
                    for entity in edit_gift_window.add_gift_item_list:
                        if edit_gift_window.compare_entity(entity, self.item_list[row]):
                            delete_entity = entity
                            break
                    edit_gift_window.add_gift_item_list.remove(delete_entity)
                    self.set_table_widget_item_state(row, False)
            self.parent().set_table_widget()
            self.tableWidget.clearSelection()
        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.click_add_gift_wall()
        else:
            super().keyPressEvent(event)

    def click_add_gift_wall(self):
        selected_rows = []
        for item in self.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        for row in selected_rows:
            self.add_gift_item(row)
        self.tableWidget.clearSelection()

    def add_gift_item(self, row):
        index = len(edit_gift_window.add_gift_item_list)
        entity = self.item_list[row]
        if edit_gift_window.is_entity_added(entity):
            return
        edit_gift_window.add_gift_item_list.append(entity)
        self.parent().tableWidget.setRowCount(len(edit_gift_window.add_gift_item_list))
        self.parent().set_table_widget_item(index, entity)
        self.parent().tableWidget.selectRow(index)
        self.set_table_widget_item_state(row, True)


def click_edit_view_radio_button(add_gift_view, type_value, radio_button_list):
    if radio_button_list:
        for radio_button in radio_button_list:
            if radio_button.isChecked():
                if type_value == 0:
                    if add_gift_view.select_language == radio_button.text():
                        return
                    add_gift_view.select_language = radio_button.text()
                else:
                    if add_gift_view.select_gift_name == radio_button.text():
                        return
                    add_gift_view.select_gift_name = radio_button.text()
        print("选择 文件夹 = %s 文件名 = %s" % (add_gift_view.select_language, add_gift_view.select_gift_name))
        add_gift_view.set_table_widget()