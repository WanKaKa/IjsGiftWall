from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QDialog
from PyQt5 import QtCore

from app.edit_gift.core import download, urls
from util import path_ex, utils

from app.edit_gift.gui.dialog import add_gift_ui


class QAddGiftDialog(QDialog, add_gift_ui.Ui_Dialog):
    __OVERALL_GIFT_WALL_FILE_NAME = "总表"

    __select_language = urls.LANGUAGE_LIST[0]
    __select_gift_name = __OVERALL_GIFT_WALL_FILE_NAME

    def __init__(self, parent=None, add_gift_item_list=None):
        super(QAddGiftDialog, self).__init__(parent)
        self.setupUi(self)

        self.add_gift_item_list = add_gift_item_list
        self.add_single_gift_callback = None
        self.add_multiple_gift_callback = None
        self.modify_gift_callback = None

        self.__server_gift_wall_file = [self.__OVERALL_GIFT_WALL_FILE_NAME]
        for file in urls.XML_NAME_LIST:
            self.__server_gift_wall_file.append(file)
        self.__show_gift_item_list = []

        self.__language_radio_list = [
            self.language_radio_1,
            self.language_radio_3,
            self.language_radio_5,
            self.language_radio_7,
            self.language_radio_9,
            self.language_radio_11,
            self.language_radio_2,
            self.language_radio_4,
            self.language_radio_6,
            self.language_radio_8,
            self.language_radio_10,
            self.language_radio_12,
        ]
        self.__file_name_radio_list = [
            self.file_name_radio_1,
            self.file_name_radio_3,
            self.file_name_radio_5,
            self.file_name_radio_7,
            self.file_name_radio_9,
            self.file_name_radio_11,
            self.file_name_radio_2,
            self.file_name_radio_4,
            self.file_name_radio_6,
            self.file_name_radio_8,
            self.file_name_radio_10,
            self.file_name_radio_12,
        ]
        self.__init_view()

        self.tableWidget.keyPressEvent = self.__key_press_event
        self.tableWidget.itemClicked.connect(self.__table_widget_item_click)
        self.tableWidget.itemDoubleClicked.connect(self.__table_widget_item_double_click)
        self.add.clicked.connect(self.__add_gift_wall)
        self.add_all.clicked.connect(self.__add_all_gift_wall)

    def __init_view(self):
        self.__init_radio_button(0, self.__language_radio_list, urls.LANGUAGE_LIST)
        self.__init_radio_button(1, self.__file_name_radio_list, self.__server_gift_wall_file)

        self.__init_table_widget()
        self.__set_table_widget()

    def __init_radio_button(self, type_value, radio_list, string_list):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(string_list)):
            utils.set_radio_button_style_10pt(radio_list[i], False)
            radio_list[i].setText(_translate("Form", string_list[i]))
            if type_value == 0:
                if self.__select_language == radio_list[i].text():
                    radio_list[i].setChecked(True)
            else:
                if self.__select_gift_name == radio_list[i].text():
                    radio_list[i].setChecked(True)
            radio_list[i].toggled.connect(
                lambda: self.__radio_button_click(type_value, radio_list))
        # 隐藏多出来的按钮
        if len(radio_list) > len(string_list):
            for i in range(len(radio_list)):
                if i >= len(string_list):
                    radio_list[i].hide()

    def __radio_button_click(self, type_value, radio_button_list):
        if radio_button_list:
            for radio_button in radio_button_list:
                if radio_button.isChecked():
                    if type_value == 0:
                        if self.__select_language == radio_button.text():
                            return
                        self.__select_language = radio_button.text()
                    else:
                        if self.__select_gift_name == radio_button.text():
                            return
                        self.__select_gift_name = radio_button.text()
            print("选择 文件夹 = %s 文件名 = %s" % (self.__select_language, self.__select_gift_name))
            self.__set_table_widget()

    def __init_table_widget(self):
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

    def __set_table_widget(self):
        if self.__show_gift_item_list:
            self.__show_gift_item_list.clear()
        if download.overall_gift_entity and download.overall_gift_entity.item_list:
            if self.__OVERALL_GIFT_WALL_FILE_NAME == self.__select_gift_name:
                self.__show_gift_item_list = download.overall_gift_entity.item_list[:]
            else:
                if self.__select_gift_name in download.gift_entity_list[self.__select_language]:
                    gift_entity = download.gift_entity_list[self.__select_language][self.__select_gift_name]
                    if gift_entity and gift_entity.item_list:
                        for item1 in gift_entity.item_list:
                            for item2 in download.overall_gift_entity.item_list:
                                if utils.compare_entity(item1, item2):
                                    self.__show_gift_item_list.append(item2)
                                    break
        if self.__show_gift_item_list:
            self.tableWidget.setRowCount(len(self.__show_gift_item_list))
            for i in range(len(self.__show_gift_item_list)):
                self.__set_table_widget_item(i, self.__show_gift_item_list[i])
        else:
            self.tableWidget.setRowCount(0)

    def __set_table_widget_item(self, index, entity_):
        self.tableWidget.setRowHeight(index, 40)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 18))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(str(index + 1))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 0, item)

        item = QTableWidgetItem()
        icon_ = QIcon(path_ex.get_download() + entity_.icon_image_path)
        item.setIcon(icon_)
        self.tableWidget.setItem(index, 1, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(entity_.project_name)
        self.tableWidget.setItem(index, 2, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setText("产品名: " + (entity_.title if entity_.title else "") +
                     "\n类   型: " + (entity_.app_type if entity_.app_type else ""))
        self.tableWidget.setItem(index, 3, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setText(entity_.package_name)
        self.tableWidget.setItem(index, 4, item)

        item = None
        if entity_.poster_path:
            item = QTableWidgetItem()
            icon_ = QIcon(path_ex.get_download() + entity_.poster_path)
            item.setIcon(QIcon(icon_))
        self.tableWidget.setItem(index, 5, item)

        self.__set_table_widget_item_state(index, utils.is_entity_added(entity_, self.add_gift_item_list))

    def __set_table_widget_item_state(self, index, state):
        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setForeground(QBrush(QColor(255, 0, 0)))
        item.setText("已添加" if state else "")
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 6, item)

    def __key_press_event(self, event):
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
                    for entity_ in self.add_gift_item_list:
                        if utils.compare_entity(entity_, self.__show_gift_item_list[row]):
                            delete_entity = entity_
                            break
                    self.add_gift_item_list.remove(delete_entity)
                    self.__set_table_widget_item_state(row, False)
            self.tableWidget.clearSelection()
            if self.modify_gift_callback:
                self.modify_gift_callback()
        elif event.key() == QtCore.Qt.Key_Enter or event.key() == QtCore.Qt.Key_Return:
            self.__add_gift_wall()
        else:
            super().keyPressEvent(event)

    def __table_widget_item_click(self):
        print(self.tableWidget.currentItem().text())

    def __table_widget_item_double_click(self):
        row = self.tableWidget.currentItem().row()
        if 0 <= row < len(self.__show_gift_item_list):
            self.__add_gift_wall_item(row)

    def __add_gift_wall(self):
        selected_rows = []
        for item in self.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        for row in selected_rows:
            self.__add_gift_wall_item(row)
        self.tableWidget.clearSelection()

    def __add_gift_wall_item(self, row):
        entity_ = self.__show_gift_item_list[row]
        if utils.is_entity_added(entity_, self.add_gift_item_list):
            return
        self.add_gift_item_list.append(entity_)
        self.__set_table_widget_item_state(row, True)
        if self.add_single_gift_callback:
            self.add_single_gift_callback(entity_)

    def __add_all_gift_wall(self):
        self.tableWidget.selectAll()
        self.__add_gift_wall()

    def set_add_single_gift_callback(self, callback=None):
        self.add_single_gift_callback = callback

    def set_add_multiple_gift_callback(self, callback=None):
        self.add_multiple_gift_callback = callback

    def set_modify_gift_callback(self, callback=None):
        self.modify_gift_callback = callback
