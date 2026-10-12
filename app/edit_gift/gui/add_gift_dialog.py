from copy import deepcopy

from PyQt5.QtCore import QSize, Qt
from PyQt5.QtGui import QFont, QFontMetrics, QBrush, QColor
from PyQt5.QtWidgets import QAbstractItemView, QTableWidgetItem, QDialog, QApplication, QMessageBox
from PyQt5 import QtCore

from app.edit_gift.core import download, urls
from util import path_pro, utils, icon, ui_scale

from app.edit_gift.gui.qt5.dialog import add_gift_ui
from app.edit_gift.gui.see_image_dialog import QSeeImageDialog
from app.edit_gift.gui.add_to_multiple_dialog import QAddToMultipleDialog


class QAddGiftDialog(QDialog, add_gift_ui.Ui_Dialog):
    __OVERALL_GIFT_WALL_FILE_NAME = "总表"

    __select_language = urls.LANGUAGE_LIST[0]
    __select_gift_name = __OVERALL_GIFT_WALL_FILE_NAME

    def __init__(self, parent=None, add_gift_item_list=None):
        super(QAddGiftDialog, self).__init__(parent)
        self.setupUi(self)

        # 获取屏幕的高度；加宽以完整显示 showTarget / 添加状态列
        screen = QApplication.primaryScreen()
        self.resize(1360, screen.availableGeometry().height() - 128)

        self.add_gift_item_list = add_gift_item_list
        self.add_single_gift_callback = None
        self.add_multiple_gift_callback = None
        self.modify_gift_callback = None

        self.__server_gift_wall_file = [self.__OVERALL_GIFT_WALL_FILE_NAME]
        for file in urls.XML_NAME_LIST_2:
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
            self.file_name_radio_13,
            self.file_name_radio_14,
            self.file_name_radio_15,
            self.file_name_radio_16,
            self.file_name_radio_17,
            self.file_name_radio_18,
        ]
        self.__init_view()

        self.tableWidget.keyPressEvent = self.__key_press_event
        self.tableWidget.itemClicked.connect(self.__table_widget_item_click)
        self.tableWidget.itemDoubleClicked.connect(self.__table_widget_item_double_click)
        self.add.clicked.connect(self.__add_gift_wall)
        self.add_multiple.clicked.connect(self.__add_all_gift_wall)
        self.close_button.clicked.connect(self.close)

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
        for i in range(len(string_list)):
            if not string_list[i]:
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
        self.tableWidget.verticalHeader().setVisible(False)
        # 项目名 / 包名过长时换行，不显示省略号
        self.tableWidget.setWordWrap(True)
        self.tableWidget.setTextElideMode(Qt.ElideNone)

        self.tableWidget.setColumnCount(8)
        self.tableWidget.setHorizontalHeaderLabels(
            ['序号', '图标', '项目名', '产品名 类型', '包名', 'showTarget', '推广图', "添加状态"])
        header_font = QFont('微软雅黑')
        header_font.setPixelSize(14)
        header = self.tableWidget.horizontalHeader()
        header.setFont(header_font)
        header.setFixedHeight(36)
        for col in range(self.tableWidget.columnCount()):
            item = self.tableWidget.horizontalHeaderItem(col)
            if item is not None:
                item.setFont(header_font)
        self.tableWidget.setStyleSheet(
            (self.tableWidget.styleSheet() or "") +
            """
            QHeaderView::section {
                font-family: "微软雅黑";
                font-size: 14px;
                padding: 4px;
            }
            """
        )
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.tableWidget.setIconSize(QSize(36, 36))
        self.tableWidget.setColumnWidth(0, 60)
        self.tableWidget.setColumnWidth(1, 60)
        self.tableWidget.setColumnWidth(2, 240)
        self.tableWidget.setColumnWidth(3, 270)
        self.tableWidget.setColumnWidth(4, 280)
        self.tableWidget.setColumnWidth(5, 120)
        self.tableWidget.setColumnWidth(6, 60)
        self.tableWidget.setColumnWidth(7, 120)

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
                                    item = deepcopy(item2)
                                    item.show_target = item1.show_target
                                    self.__show_gift_item_list.append(item)
                                    break
        if self.__show_gift_item_list:
            self.tableWidget.setRowCount(len(self.__show_gift_item_list))
            for i in range(len(self.__show_gift_item_list)):
                self.__set_table_widget_item(i, self.__show_gift_item_list[i])
            self.__fit_table_row_heights()
        else:
            self.tableWidget.setRowCount(0)

    def __fit_table_row_heights(self):
        """按换行内容自适应行高，且不低于图标所需高度。"""
        min_h = max(
            ui_scale.scaled_px(40),
            self.tableWidget.iconSize().height() + ui_scale.scaled_px(8),
        )
        for row in range(self.tableWidget.rowCount()):
            self.tableWidget.resizeRowToContents(row)
            if self.tableWidget.rowHeight(row) < min_h:
                self.tableWidget.setRowHeight(row, min_h)

    def __wrap_text_for_column(self, text, column, font):
        """按列宽插入换行，避免长项目名/包名显示省略号或被裁切。"""
        text = text or ""
        if not text:
            return text
        # 预留单元格左右内边距
        max_width = max(20, self.tableWidget.columnWidth(column) - ui_scale.scaled_px(12))
        metrics = QFontMetrics(font)
        lines = []
        current = ""
        for ch in text:
            trial = current + ch
            if current and metrics.horizontalAdvance(trial) > max_width:
                lines.append(current)
                current = ch
            else:
                current = trial
        if current:
            lines.append(current)
        return "\n".join(lines)

    def __set_table_widget_item(self, index, entity_):
        item = QTableWidgetItem()
        item.setFont(ui_scale.make_font('微软雅黑', 18))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(str(index + 1))
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 0, item)

        item = QTableWidgetItem()
        icon_size = self.tableWidget.iconSize()
        icon_ = ui_scale.scaled_icon(
            path_pro.get_download() + entity_.icon_image_path,
            icon_size,
            widget=self.tableWidget,
        )
        item.setIcon(icon_)
        self.tableWidget.setItem(index, 1, item)

        name_font = ui_scale.make_font('微软雅黑', 10)
        item = QTableWidgetItem()
        item.setFont(name_font)
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(self.__wrap_text_for_column(entity_.project_name, 2, name_font))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tableWidget.setItem(index, 2, item)

        item = QTableWidgetItem()
        item.setFont(ui_scale.make_font('微软雅黑', 10))
        item.setText("产品名: " + (entity_.title if entity_.title else "") +
                     "\n类   型: " + (entity_.app_type if entity_.app_type else ""))
        self.tableWidget.setItem(index, 3, item)

        item = QTableWidgetItem()
        item.setFont(name_font)
        item.setText(self.__wrap_text_for_column(entity_.package_name, 4, name_font))
        item.setTextAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.tableWidget.setItem(index, 4, item)

        item = QTableWidgetItem()
        item.setFont(ui_scale.make_font('微软雅黑', 10))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(entity_.show_target if entity_.show_target else "")
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 5, item)

        item = None
        if entity_.poster_path:
            item = QTableWidgetItem()
            icon_size = self.tableWidget.iconSize()
            icon_ = ui_scale.scaled_icon(
                path_pro.get_download() + entity_.poster_path,
                icon_size,
                widget=self.tableWidget,
            )
            item.setIcon(icon_)
        self.tableWidget.setItem(index, 6, item)

        self.__set_table_widget_item_state(index, utils.is_entity_added(entity_, self.add_gift_item_list))

    def __set_table_widget_item_state(self, index, state):
        item = QTableWidgetItem()
        item.setFont(ui_scale.make_font('微软雅黑', 12))
        item.setForeground(QBrush(QColor(255, 0, 0)))
        item.setText("已添加" if state else "")
        item.setTextAlignment(Qt.AlignCenter)
        self.tableWidget.setItem(index, 7, item)

    def __key_press_event(self, event):
        if event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            self.tableWidget.selectAll()
        elif event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_D:
            selected_rows = []
            for item in self.tableWidget.selectedItems():
                if item.row() not in selected_rows:
                    selected_rows.append(item.row())
            for row in selected_rows:
                state_item = self.tableWidget.item(row, 7)
                if state_item and state_item.text():
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
        current_item = self.tableWidget.currentItem()
        if not current_item:
            return
        row = current_item.row()
        if not (0 <= row < len(self.__show_gift_item_list)):
            return
        entity_ = self.__show_gift_item_list[row]
        column = current_item.column()
        if column == 2:
            text = entity_.project_name or ""
            if text:
                QApplication.clipboard().setText(text)
                print("已复制项目名: %s" % text)
        elif column == 3:
            text = "产品名: " + (entity_.title if entity_.title else "") + \
                   "\n类   型: " + (entity_.app_type if entity_.app_type else "")
            QApplication.clipboard().setText(text)
            print("已复制产品名和类型: %s" % text.replace("\n", " / "))
        elif column == 4:
            text = entity_.package_name or ""
            if text:
                QApplication.clipboard().setText(text)
                print("已复制包名: %s" % text)
        elif column == 6:
            self.__show_poster_dialog(entity_)

    def __show_poster_dialog(self, entity_):
        if not entity_ or not entity_.poster_path:
            return
        dialog = QSeeImageDialog(self)
        if entity_.icon_image_path:
            ui_scale.set_label_pixmap(
                dialog.icon, path_pro.get_download() + entity_.icon_image_path)
        ui_scale.set_label_pixmap(
            dialog.poster,
            path_pro.get_download() + entity_.poster_path,
            dialog.poster.maximumSize().width(),
            dialog.poster.maximumSize().height(),
        )
        dialog.setWindowTitle("推广图")
        dialog.exec_()

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
        # 添加时不拷贝 showTarget，需用户在主列表手动选择
        new_entity = deepcopy(entity_)
        new_entity.show_target = None
        self.add_gift_item_list.append(new_entity)
        self.__set_table_widget_item_state(row, True)
        if self.add_single_gift_callback:
            self.add_single_gift_callback(new_entity)

    def __add_all_gift_wall(self):
        selected_rows = []
        for item in self.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        if not selected_rows:
            QMessageBox.information(self, '提示', '请先勾选要添加的数据!')
            return

        default_file_names, default_languages = self.__get_main_selected_defaults()
        dialog = QAddToMultipleDialog(
            self,
            default_file_names=default_file_names,
            default_languages=default_languages,
        )
        dialog.setWindowIcon(icon.get_logo())
        if dialog.exec_() != QDialog.Accepted:
            return

        file_names = dialog.get_selected_file_names()
        languages = dialog.get_selected_languages()
        if not file_names:
            QMessageBox.information(self, '提示', '请选择文件名!')
            return
        if not languages:
            QMessageBox.information(self, '提示', '请选择地区!')
            return

        entity_list = []
        for row in selected_rows:
            if not (0 <= row < len(self.__show_gift_item_list)):
                continue
            new_entity = deepcopy(self.__show_gift_item_list[row])
            new_entity.show_target = None
            entity_list.append(new_entity)
        if not entity_list:
            QMessageBox.information(self, '提示', '没有可添加的数据!')
            return

        if self.add_multiple_gift_callback:
            self.add_multiple_gift_callback(entity_list, file_names, languages)

        for row in selected_rows:
            if 0 <= row < len(self.__show_gift_item_list):
                self.__set_table_widget_item_state(
                    row, utils.is_entity_added(self.__show_gift_item_list[row], self.add_gift_item_list))
        self.tableWidget.clearSelection()

    def __get_main_selected_defaults(self):
        file_names = []
        languages = []
        parent = self.parent()
        if parent and hasattr(parent, "edit_language"):
            file_text = (parent.edit_language.ui.file_name.text() or "").strip()
            if file_text:
                for name in file_text.split(","):
                    name = name.strip()
                    if name:
                        file_names.append(name)
            language_text = (parent.edit_language.ui.language.text() or "").strip()
            if language_text:
                for language in language_text.split(","):
                    language = language.strip()
                    if language:
                        languages.append(language)
        return file_names, languages

    def refresh_after_ui_scale(self):
        """比例抛光后按新的 iconSize/列宽重绘表格内容。"""
        self.__set_table_widget()

    def set_add_single_gift_callback(self, callback=None):
        self.add_single_gift_callback = callback

    def set_add_multiple_gift_callback(self, callback=None):
        self.add_multiple_gift_callback = callback

    def set_modify_gift_callback(self, callback=None):
        self.modify_gift_callback = callback
