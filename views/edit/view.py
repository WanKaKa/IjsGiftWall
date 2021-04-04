import os
import shutil

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor, QPixmap
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QDialog
from PyQt5 import QtCore

from database import database_json
from utils import path_utils, ico_utils, gift_xml_utils, kevin_utils
from views.edit import edit_gift_ui, add_gift
import giftdata
from views import dialog
from giftdata import urls
from giftdata.entity import GiftConfig

add_gift_item_list = []
add_gift_config_list = {
    gift_xml_utils.TARGET_RATE: GiftConfig(target=gift_xml_utils.TARGET_RATE),
    gift_xml_utils.TARGET_INTERSTITIAL: GiftConfig(target=gift_xml_utils.TARGET_INTERSTITIAL),
    gift_xml_utils.TARGET_LIST: GiftConfig(target=gift_xml_utils.TARGET_LIST),
    gift_xml_utils.TARGET_DIALOG: GiftConfig(target=gift_xml_utils.TARGET_DIALOG),
    gift_xml_utils.TARGET_CAROUSEL: GiftConfig(target=gift_xml_utils.TARGET_CAROUSEL, count='10000'),
    gift_xml_utils.TARGET_SIDEBAR: GiftConfig(target=gift_xml_utils.TARGET_SIDEBAR),
    gift_xml_utils.TARGET_WALL: GiftConfig(target=gift_xml_utils.TARGET_WALL, count=None, limit=None),
}


class EditGiftView(QWidget, edit_gift_ui.Ui_Form):
    def __init__(self, parent=None):
        super(EditGiftView, self).__init__(parent)
        self.setupUi(self)

        self.setWindowTitle("广告配置编辑-为便捷而生")
        self.setWindowIcon(ico_utils.get_favicon_icon())

        pix_map = QPixmap(ico_utils.resource_path(os.path.join("ico", "logo.png")))
        self.ijoysoft_icon.setPixmap(pix_map)

        self.tableWidget.keyPressEvent = self.key_press_event
        self.pushButton.clicked.connect(lambda: click_set_out_file(self))
        self.pushButton_2.clicked.connect(lambda: click_set_language(self))
        self.refresh_ui.clicked.connect(self.init_view)
        self.reload_data.clicked.connect(lambda: click_reload_data(self))
        self.add_gift_wall.clicked.connect(lambda: click_add_gift_wall(self))
        self.create_gift_wall_file.clicked.connect(self.click_create_gift_wall_file)
        self.open_outputs.clicked.connect(lambda: os.system("start " + path_utils.get_outputs_path()))
        self.clear_outputs.clicked.connect(self.delete_dir)

    def init_view(self):
        self.init_table_widget()
        self.set_table_widget()
        self.set_gift_config_view()

    def init_table_widget(self):
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

    def set_table_widget(self):
        if add_gift_item_list:
            self.tableWidget.setRowCount(len(add_gift_item_list))
            for i in range(len(add_gift_item_list)):
                self.set_table_widget_item(i, add_gift_item_list[i])
        else:
            self.tableWidget.setRowCount(0)

    def set_table_widget_item(self, index, entity):
        self.tableWidget.setRowHeight(index, 80)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 30))
        item.setForeground(QBrush(QColor(85, 85, 255)))
        entity.id = str(index + 1)
        item.setText(entity.id)
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

    def set_gift_config_view(self):
        value = add_gift_config_list[gift_xml_utils.TARGET_RATE]
        self.rate_index.setText(value.index)
        self.rate_count.setText(value.count)
        self.rate_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_INTERSTITIAL]
        self.interstitial_index.setText(value.index)
        self.interstitial_count.setText(value.count)
        self.interstitial_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_LIST]
        self.list_index.setText(value.index)
        self.list_count.setText(value.count)
        self.list_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_DIALOG]
        self.dialog_index.setText(value.index)
        self.dialog_count.setText(value.count)
        self.dialog_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_CAROUSEL]
        self.carousel_index.setText(value.index)
        self.carousel_count.setText(value.count)
        self.carousel_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_SIDEBAR]
        self.sidebar_index.setText(value.index)
        self.sidebar_count.setText(value.count)
        self.sidebar_limit.setText(value.limit)

        value = add_gift_config_list[gift_xml_utils.TARGET_WALL]
        self.wall_index.setText(value.index)

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
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            self.tableWidget.selectAll()
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

    def click_create_gift_wall_file(self):
        reply = QMessageBox.question(
            self, '生成GiftWall配置表', '确定生成GiftWall配置表吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            if not self.file_name.text():
                QMessageBox.information(self, '提示', '输出文件名为空!')
                return
            if not self.language.text():
                QMessageBox.information(self, '提示', '输出地区为空!')
                return
            if not add_gift_item_list:
                QMessageBox.information(self, '提示', '数据为空!')
                return
            if not self.set_gift_config_list():
                QMessageBox.information(self, '提示', 'GiftWall配置输入不正确!')
                return
            gift_xml_utils.create_gift_wall_files(
                self.file_name.text(), self.language.text().split(","), add_gift_config_list, add_gift_item_list)
            QMessageBox.information(self, '提示', '生成GiftWall配置表成功!')

    def set_gift_config_list(self):
        if not self.is_gift_config_valid():
            return False
        value = add_gift_config_list[gift_xml_utils.TARGET_RATE]
        value.index = self.rate_index.text()
        value.count = self.rate_count.text()
        value.limit = self.rate_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_RATE] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_INTERSTITIAL]
        value.index = self.interstitial_index.text()
        value.count = self.interstitial_count.text()
        value.limit = self.interstitial_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_INTERSTITIAL] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_LIST]
        value.index = self.list_index.text()
        value.count = self.list_count.text()
        value.limit = self.list_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_LIST] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_DIALOG]
        value.index = self.dialog_index.text()
        value.count = self.dialog_count.text()
        value.limit = self.dialog_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_DIALOG] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_CAROUSEL]
        value.index = self.carousel_index.text()
        value.count = self.carousel_count.text()
        value.limit = self.carousel_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_CAROUSEL] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_SIDEBAR]
        value.index = self.sidebar_index.text()
        value.count = self.sidebar_count.text()
        value.limit = self.sidebar_limit.text()
        add_gift_config_list[gift_xml_utils.TARGET_SIDEBAR] = value

        value = add_gift_config_list[gift_xml_utils.TARGET_WALL]
        value.index = self.wall_index.text()
        add_gift_config_list[gift_xml_utils.TARGET_WALL] = value
        return True

    def is_gift_config_valid(self):
        gift_config_input_list = [
            self.rate_index,
            self.rate_count,
            self.rate_limit,
            self.interstitial_index,
            self.interstitial_count,
            self.interstitial_limit,
            self.list_index,
            self.list_count,
            self.list_limit,
            self.dialog_index,
            self.dialog_count,
            self.dialog_limit,
            self.carousel_index,
            self.carousel_count,
            self.carousel_limit,
            self.sidebar_index,
            self.sidebar_count,
            self.sidebar_limit,
            self.wall_index,
        ]
        for gift_config_input in gift_config_input_list:
            if not gift_config_input.text() or not gift_config_input.text().isdigit():
                return False
        return True

    def delete_dir(self):
        reply = QMessageBox.question(
            self, '清空Outputs', '确定清空Outputs吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            kevin_utils.delete_dir(path_utils.get_outputs_path())
            QMessageBox.information(self, '提示', 'Outputs已清空!')


class AddGiftView(QDialog, add_gift.Ui_Dialog):
    OVERALL_GIFT_WALL_FILE_NAME = "总表"

    def __init__(self, parent=None):
        super(AddGiftView, self).__init__(parent)
        self.setupUi(self)

        self.server_gift_wall_file = [self.OVERALL_GIFT_WALL_FILE_NAME]
        for file in urls.XML_NAME_LIST:
            self.server_gift_wall_file.append(file)
        self.item_list = []
        self.init_view()

        self.tableWidget.keyPressEvent = self.key_press_event
        self.tableWidget.itemClicked.connect(self.click_table_item)
        self.tableWidget.itemDoubleClicked.connect(self.click_table_item_double)
        self.pushButton.clicked.connect(self.click_get_gift_wall_file)
        self.pushButton_2.clicked.connect(self.click_add_gift_wall)

    def init_view(self):
        self.label_2.setText(self.OVERALL_GIFT_WALL_FILE_NAME)
        self.init_table_widget()
        self.set_table_widget()

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
            if self.OVERALL_GIFT_WALL_FILE_NAME == self.label_2.text():
                self.item_list = giftdata.overall_gift_entity.item_list[:]
            else:
                if giftdata.gift_entity_list and self.label_2.text() in giftdata.gift_entity_list:
                    gift_entity = giftdata.gift_entity_list[self.label_2.text()]
                    if gift_entity and gift_entity.item_list:
                        for item1 in gift_entity.item_list:
                            for item2 in giftdata.overall_gift_entity.item_list:
                                if compare_entity(item1, item2):
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

        self.set_table_widget_item_state(index, is_entity_added(entity))

    def set_table_widget_item_state(self, index, state):
        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 16))
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
        elif event.key() == QtCore.Qt.Key_Delete:
            selected_rows = []
            for item in self.tableWidget.selectedItems():
                if item.row() not in selected_rows:
                    selected_rows.append(item.row())
            for row in selected_rows:
                if self.tableWidget.item(row, 6).text():
                    delete_entity = None
                    for entity in add_gift_item_list:
                        if compare_entity(entity, self.item_list[row]):
                            delete_entity = entity
                            break
                    add_gift_item_list.remove(delete_entity)
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
        index = len(add_gift_item_list)
        entity = self.item_list[row]
        if is_entity_added(entity):
            return
        add_gift_item_list.append(entity)
        self.parent().tableWidget.setRowCount(len(add_gift_item_list))
        self.parent().set_table_widget_item(index, entity)
        self.parent().tableWidget.selectRow(index)
        self.set_table_widget_item_state(row, True)

    def click_get_gift_wall_file(self):
        server_file_dialog = dialog.SelectDialog(self)
        server_file_dialog.show()
        server_file_dialog.setWindowTitle("选择服务器配置表-为便捷而生")
        server_file_dialog.setWindowIcon(ico_utils.get_favicon_icon())

        server_file_radio_button_list = [
            server_file_dialog.radioButton,
            server_file_dialog.radioButton_2,
            server_file_dialog.radioButton_3,
            server_file_dialog.radioButton_4,
            server_file_dialog.radioButton_5,
            server_file_dialog.radioButton_6,
            server_file_dialog.radioButton_7,
            server_file_dialog.radioButton_8,
            server_file_dialog.radioButton_9,
            server_file_dialog.radioButton_10,
            server_file_dialog.radioButton_11,
            server_file_dialog.radioButton_12,
            server_file_dialog.radioButton_13,
            server_file_dialog.radioButton_14,
            server_file_dialog.radioButton_15,
            server_file_dialog.radioButton_16
        ]
        # 设置按钮状态和点击事件
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(self.server_gift_wall_file)):
            server_file_radio_button_list[i].setText(_translate("Form", self.server_gift_wall_file[i]))
            server_file_radio_button_list[i].setChecked(self.label_2.text() == self.server_gift_wall_file[i])
            server_file_radio_button_list[i].toggled.connect(
                lambda: self.set_gift_wall_file(server_file_dialog, server_file_radio_button_list))
        # 隐藏多出来的按钮
        if len(server_file_radio_button_list) > len(self.server_gift_wall_file):
            for i in range(len(server_file_radio_button_list)):
                if i >= len(self.server_gift_wall_file):
                    server_file_radio_button_list[i].hide()
        server_file_dialog.exec()

    def set_gift_wall_file(self, server_file_dialog, server_file_radio_button_list):
        if server_file_radio_button_list:
            for radio_button in server_file_radio_button_list:
                if radio_button.isChecked():
                    self.label_2.setText(radio_button.text())
                    self.set_table_widget()
                    server_file_dialog.hide()


def click_set_out_file(edit_gift_view):
    out_file_dialog = dialog.SelectDialog(edit_gift_view)
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
            lambda: click_get_out_file(edit_gift_view, out_file_dialog, out_file_radio_button_list))
    # 隐藏多出来的按钮
    if len(out_file_radio_button_list) > len(urls.XML_NAME_LIST):
        for i in range(len(out_file_radio_button_list)):
            if i >= len(urls.XML_NAME_LIST):
                out_file_radio_button_list[i].hide()
    out_file_dialog.exec()


def click_get_out_file(edit_gift_view, out_file_dialog, out_file_radio_button_list):
    if out_file_radio_button_list:
        for radio_button in out_file_radio_button_list:
            if radio_button.isChecked():
                edit_gift_view.file_name.setText(radio_button.text())
                out_file_dialog.hide()


def click_set_language(edit_gift_view):
    language_dialog = dialog.MultipleSelectDialog(edit_gift_view)
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
            lambda: click_get_language(edit_gift_view, language_check_box_list))
    # 隐藏多出来的按钮
    if len(language_check_box_list) > len(urls.LANGUAGE_LIST):
        for i in range(len(language_check_box_list)):
            if i >= len(urls.LANGUAGE_LIST):
                language_check_box_list[i].hide()
    language_dialog.deselect_all.clicked.connect(lambda: click_select_all_language(language_check_box_list, False))
    language_dialog.select_all.clicked.connect(lambda: click_select_all_language(language_check_box_list, True))
    language_dialog.ok.clicked.connect(lambda: language_dialog.hide())
    language_dialog.exec()


def click_get_language(edit_gift_view, language_check_box_list):
    if language_check_box_list:
        edit_gift_view.language.setText("")
        for radio_button in language_check_box_list:
            if radio_button.isChecked():
                edit_gift_view.language.setText(edit_gift_view.language.text() + radio_button.text().strip(" ") + ",")


def click_select_all_language(language_check_box_list, enable):
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setChecked(enable)


def click_reload_data(edit_gift_view):
    reply = QMessageBox.question(edit_gift_view, '重新下载', '确认重新下载服务器数据吗?', QMessageBox.No | QMessageBox.Yes,
                                 QMessageBox.No)
    if reply == QMessageBox.Yes:
        database_json.save(database_json.KEY_GIFT_DATA_UPDATE_TIME, 0)
        database_json.save(database_json.KEY_GIFT_ICON_UPDATE_TIME, 0)
        giftdata.download.load_config()


def is_entity_added(entity):
    title1 = entity.title if entity.title else ""
    package_name1 = entity.package_name if entity.package_name else ""
    for value in add_gift_item_list:
        title2 = value.title if value.title else ""
        package_name2 = value.package_name if value.package_name else ""
        if title1 == title2 and package_name1 == package_name2:
            return True
    return False


def compare_entity(entity1, entity2):
    title1 = entity1.title if entity1.title else ""
    package_name1 = entity1.package_name if entity1.package_name else ""
    title2 = entity2.title if entity2.title else ""
    package_name2 = entity2.package_name if entity2.package_name else ""
    return title1 == title2 and package_name1 == package_name2


def click_add_gift_wall(edit_gift_view):
    add_gift_view = AddGiftView(edit_gift_view)
    add_gift_view.setWindowTitle("添加GiftWall-为便捷而生")
    add_gift_view.setWindowIcon(ico_utils.get_favicon_icon())
    add_gift_view.exec()
