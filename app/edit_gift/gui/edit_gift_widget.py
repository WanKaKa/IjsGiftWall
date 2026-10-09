import os
import threading
import time

from copy import deepcopy
from PyQt5.QtCore import QSize, Qt, QUrl
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor, QPixmap, QDesktopServices
from PyQt5.QtWidgets import (
    QWidget, QAbstractItemView, QTableWidgetItem, QMessageBox, QStyle, QFileDialog,
    QApplication, QPushButton, QHBoxLayout, QVBoxLayout, QSizePolicy, QDialog, QLabel
)
from PyQt5 import QtCore

from app.edit_gift.core.download import DownloadConfig
from database import json_pro
from app.edit_gift.core import entity, download, urls, xml_pro
from util import path_pro, icon, utils

from app.edit_gift.gui.add_gift_dialog import QAddGiftDialog
from app.edit_gift.gui.progress_dialog import QProgressDialog
from app.edit_gift.gui.see_image_dialog import QSeeImageDialog
from app.edit_gift.gui.single_select_dialog import QSingleSelectDialog
from app.edit_gift.gui.multiple_select_dialog import QMultipleSelectDialog
from app.edit_gift.gui.qt5.operation import edit_language_ui, edit_button_ui, check_button_ui, check_language_ui
from app.edit_gift.gui.qt5 import table_widget_ui, edit_gift_ui

DEFAULT_GIFT_CONFIG_LIST = {
    xml_pro.TARGET_RATE: entity.GiftConfig(target=xml_pro.TARGET_RATE, limit='5'),
    xml_pro.TARGET_BANNER: entity.GiftConfig(target=xml_pro.TARGET_BANNER, count='0', limit='3'),
    xml_pro.TARGET_INTERSTITIAL: entity.GiftConfig(target=xml_pro.TARGET_INTERSTITIAL, count='0', limit='3'),
    xml_pro.TARGET_LIST: entity.GiftConfig(target=xml_pro.TARGET_LIST, count='0', limit='3'),
    xml_pro.TARGET_DIALOG: entity.GiftConfig(target=xml_pro.TARGET_DIALOG, limit='1'),
    xml_pro.TARGET_CAROUSEL: entity.GiftConfig(target=xml_pro.TARGET_CAROUSEL, count='10000'),
    xml_pro.TARGET_SIDEBAR: entity.GiftConfig(target=xml_pro.TARGET_SIDEBAR, count='3'),
    xml_pro.TARGET_WALL: entity.GiftConfig(target=xml_pro.TARGET_WALL, count=None, limit=None),
}

# 0: 编辑模式 1: 查看模式
select_mode_type = 0
# GiftItem列表数据
add_gift_item_list = []
# gift wall配置数据
add_gift_config_list = deepcopy(DEFAULT_GIFT_CONFIG_LIST)


class QEditGiftWidget(QWidget):
    def __init__(self, parent: QWidget):
        super(QEditGiftWidget, self).__init__(parent)
        self.ui = edit_gift_ui.Ui_Form()
        self.ui.setupUi(self)

        self.setWindowState(Qt.WindowMaximized)
        self.progress_dialog = QProgressDialog(self)

        # 设置公司Logo
        pix_map = QPixmap(icon.resource_path(os.path.join("ico", "logo_big.png")))
        self.ui.ijoysoft_icon.setPixmap(pix_map)

        utils.set_radio_button_style_10pt(self.ui.edit_gift_wall_mode, False)
        utils.set_radio_button_style_10pt(self.ui.check_outputs_mode, False)
        utils.set_radio_button_style_10pt(self.ui.server_url_1, False)
        utils.set_radio_button_style_10pt(self.ui.server_url_2, False)

        # 模式切换点击事件
        self.ui.edit_gift_wall_mode.toggled.connect(lambda: self.switch_mode())
        self.ui.check_outputs_mode.toggled.connect(lambda: self.switch_mode())

        self.ui.server_url_1.toggled.connect(lambda: self.switch_server_url())
        self.ui.server_url_2.toggled.connect(lambda: self.switch_server_url())

        if urls.ALIYUN_SERVER_URL == json_pro.get_selected_server_url():
            self.ui.server_url_1.setChecked(True)
        else:
            self.ui.server_url_2.setChecked(True)

        # 不同模式下的地区和文件名选择
        self.edit_language = QEditLanguage(parent=self)
        self.ui.edit_check_language_layout.addWidget(self.edit_language)
        self.check_language = QCheckLanguage(parent=self)
        self.ui.edit_check_language_layout.addWidget(self.check_language)

        # 显示列表
        self.content = QKevinTableWidget(parent=self)
        self.ui.content_layout.addWidget(self.content)

        # 不同模式下的按钮设置
        self.edit_operation = QEditOperation(parent=self)
        self.ui.edit_check_menu_layout.addWidget(self.edit_operation)
        self.check_operation = QCheckOperation(parent=self)
        self.ui.edit_check_menu_layout.addWidget(self.check_operation)

        # 用于判断检查模式下是否有未保存修改
        self._saved_state = None

    def init_view(self):
        self.content.set_table_widget()
        if select_mode_type == 0:
            self.ui.edit_gift_wall_mode.setChecked(True)
            self.ui.check_outputs_mode.setChecked(False)
        else:
            self.ui.edit_gift_wall_mode.setChecked(False)
            self.ui.check_outputs_mode.setChecked(True)
        self.set_select_mode()
        self.set_gift_config_view()
        self.mark_saved_state()

    def set_select_mode(self):
        if select_mode_type == 0:
            self.edit_language.show()
            self.check_language.hide()
            # self.ui.mode_frame.setStyleSheet("background-color: rgb(57, 61, 255);")
            self.check_operation.setVisible(False)
            self.edit_operation.setVisible(True)
        else:
            self.edit_language.hide()
            self.check_language.show()
            # self.ui.mode_frame.setStyleSheet("background-color: rgb(0, 170, 0);")
            self.edit_operation.setVisible(False)
            self.check_operation.setVisible(True)

    def set_gift_config_view(self):
        value = add_gift_config_list[xml_pro.TARGET_RATE]
        self.ui.rate_index.setText(value.index)
        self.ui.rate_count.setText(value.count)
        self.ui.rate_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_BANNER]
        self.ui.banner_index.setText(value.index)
        self.ui.banner_count.setText(value.count)
        self.ui.banner_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_INTERSTITIAL]
        self.ui.interstitial_index.setText(value.index)
        self.ui.interstitial_count.setText(value.count)
        self.ui.interstitial_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_LIST]
        self.ui.list_index.setText(value.index)
        self.ui.list_count.setText(value.count)
        self.ui.list_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_DIALOG]
        self.ui.dialog_index.setText(value.index)
        self.ui.dialog_count.setText(value.count)
        self.ui.dialog_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_CAROUSEL]
        self.ui.carousel_index.setText(value.index)
        self.ui.carousel_count.setText(value.count)
        self.ui.carousel_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_SIDEBAR]
        self.ui.sidebar_index.setText(value.index)
        self.ui.sidebar_count.setText(value.count)
        self.ui.sidebar_limit.setText(value.limit)

        value = add_gift_config_list[xml_pro.TARGET_WALL]
        self.ui.wall_index.setText(value.index)

    def _config_ui_snapshot(self):
        return (
            self.ui.rate_index.text(), self.ui.rate_count.text(), self.ui.rate_limit.text(),
            self.ui.banner_index.text(), self.ui.banner_count.text(), self.ui.banner_limit.text(),
            self.ui.interstitial_index.text(), self.ui.interstitial_count.text(), self.ui.interstitial_limit.text(),
            self.ui.list_index.text(), self.ui.list_count.text(), self.ui.list_limit.text(),
            self.ui.dialog_index.text(), self.ui.dialog_count.text(), self.ui.dialog_limit.text(),
            self.ui.carousel_index.text(), self.ui.carousel_count.text(), self.ui.carousel_limit.text(),
            self.ui.sidebar_index.text(), self.ui.sidebar_count.text(), self.ui.sidebar_limit.text(),
            self.ui.wall_index.text(),
        )

    def get_state_snapshot(self):
        items = tuple(
            (item.package_name or "", item.title or "", item.show_target or "")
            for item in add_gift_item_list
        )
        return items, self._config_ui_snapshot()

    def mark_saved_state(self):
        self._saved_state = self.get_state_snapshot()

    def has_unsaved_changes(self):
        if self._saved_state is None:
            return False
        return self.get_state_snapshot() != self._saved_state

    def confirm_unsaved_changes(self):
        """左：取消修改(红)；右：保存修改(蓝)。关闭窗口视为中止切换。"""
        dialog = QDialog(self)
        dialog.setWindowTitle("提示")
        dialog.setWindowIcon(icon.get_logo())
        dialog.setMinimumWidth(360)
        root = QVBoxLayout(dialog)
        root.setContentsMargins(24, 16, 24, 20)
        root.setSpacing(0)
        tip = QLabel("当前文件有未保存的修改，请选择：")
        tip.setStyleSheet("font: 12pt \"微软雅黑\";")
        tip.setAlignment(Qt.AlignCenter)
        root.addSpacing(20)
        root.addWidget(tip)
        root.addSpacing(28)

        btn_row = QHBoxLayout()
        discard_btn = QPushButton("取消修改")
        discard_btn.setFixedSize(120, 40)
        discard_btn.setStyleSheet(
            "background-color: rgb(255, 0, 0); color: rgb(255, 255, 255); font: 12pt \"微软雅黑\";")
        save_btn = QPushButton("保存修改")
        save_btn.setFixedSize(120, 40)
        save_btn.setStyleSheet(
            "background-color: rgb(57, 61, 255); color: rgb(255, 255, 255); font: 12pt \"微软雅黑\";")
        btn_row.addWidget(discard_btn)
        btn_row.addStretch(1)
        btn_row.addWidget(save_btn)
        root.addLayout(btn_row)

        result = ["cancel"]
        discard_btn.clicked.connect(lambda: (result.__setitem__(0, "discard"), dialog.accept()))
        save_btn.clicked.connect(lambda: (result.__setitem__(0, "save"), dialog.accept()))
        dialog.exec_()
        return result[0]

    def ensure_unsaved_handled(self):
        """处理未保存修改。保存/取消修改后停留在当前界面，不继续切换。
        返回 True 表示无未保存修改可继续切换，False 表示已处理或中止、勿切换。"""
        if not self.has_unsaved_changes():
            return True
        choice = self.confirm_unsaved_changes()
        if choice == "save":
            self.save_gift_wall_file(show_tip=False)
        elif choice == "discard":
            # 放弃修改：重新加载当前文件，留在当前界面
            self.load_outputs_xml_file()
        return False

    def _revert_mode_radio(self):
        self.ui.edit_gift_wall_mode.blockSignals(True)
        self.ui.check_outputs_mode.blockSignals(True)
        if select_mode_type == 0:
            self.ui.edit_gift_wall_mode.setChecked(True)
            self.ui.check_outputs_mode.setChecked(False)
        else:
            self.ui.edit_gift_wall_mode.setChecked(False)
            self.ui.check_outputs_mode.setChecked(True)
        self.ui.edit_gift_wall_mode.blockSignals(False)
        self.ui.check_outputs_mode.blockSignals(False)

    def save_gift_wall_file(self, show_tip=True):
        if not self.edit_language.ui.file_name.text():
            QMessageBox.information(self, '提示', '输出文件名为空!')
            return False
        if not self.edit_language.ui.language.text():
            QMessageBox.information(self, '提示', '输出地区为空!')
            return False
        if not add_gift_item_list:
            QMessageBox.information(self, '提示', '数据为空!')
            return False
        if not self.get_gift_config_list():
            QMessageBox.information(self, '提示', 'GiftWall配置输入不正确!')
            return False
        xml_pro.create_gift_wall_files(self.edit_language.ui.file_name.text(),
                                      self.edit_language.ui.language.text().split(","),
                                      add_gift_config_list, add_gift_item_list)
        # 每次生成文件后，更新输出文件夹中的文件夹集合
        self.check_language.set_radio_button_color()
        self.mark_saved_state()
        if show_tip:
            QMessageBox.information(self, '提示', '生成GiftWall配置表成功!')
        return True

    def get_gift_config_list(self):
        if not self.is_gift_config_valid():
            return False
        value = add_gift_config_list[xml_pro.TARGET_RATE]
        value.index = self.ui.rate_index.text()
        value.count = self.ui.rate_count.text()
        value.limit = self.ui.rate_limit.text()
        add_gift_config_list[xml_pro.TARGET_RATE] = value

        value = add_gift_config_list[xml_pro.TARGET_BANNER]
        value.index = self.ui.banner_index.text()
        value.count = self.ui.banner_count.text()
        value.limit = self.ui.banner_limit.text()
        add_gift_config_list[xml_pro.TARGET_BANNER] = value

        value = add_gift_config_list[xml_pro.TARGET_INTERSTITIAL]
        value.index = self.ui.interstitial_index.text()
        value.count = self.ui.interstitial_count.text()
        value.limit = self.ui.interstitial_limit.text()
        add_gift_config_list[xml_pro.TARGET_INTERSTITIAL] = value

        value = add_gift_config_list[xml_pro.TARGET_LIST]
        value.index = self.ui.list_index.text()
        value.count = self.ui.list_count.text()
        value.limit = self.ui.list_limit.text()
        add_gift_config_list[xml_pro.TARGET_LIST] = value

        value = add_gift_config_list[xml_pro.TARGET_DIALOG]
        value.index = self.ui.dialog_index.text()
        value.count = self.ui.dialog_count.text()
        value.limit = self.ui.dialog_limit.text()
        add_gift_config_list[xml_pro.TARGET_DIALOG] = value

        value = add_gift_config_list[xml_pro.TARGET_CAROUSEL]
        value.index = self.ui.carousel_index.text()
        value.count = self.ui.carousel_count.text()
        value.limit = self.ui.carousel_limit.text()
        add_gift_config_list[xml_pro.TARGET_CAROUSEL] = value

        value = add_gift_config_list[xml_pro.TARGET_SIDEBAR]
        value.index = self.ui.sidebar_index.text()
        value.count = self.ui.sidebar_count.text()
        value.limit = self.ui.sidebar_limit.text()
        add_gift_config_list[xml_pro.TARGET_SIDEBAR] = value

        value = add_gift_config_list[xml_pro.TARGET_WALL]
        value.index = self.ui.wall_index.text()
        add_gift_config_list[xml_pro.TARGET_WALL] = value
        return True

    def is_gift_config_valid(self):
        gift_config_input_list = [
            self.ui.rate_index,
            self.ui.rate_count,
            self.ui.rate_limit,
            self.ui.interstitial_index,
            self.ui.interstitial_count,
            self.ui.interstitial_limit,
            self.ui.list_index,
            self.ui.list_count,
            self.ui.list_limit,
            self.ui.dialog_index,
            self.ui.dialog_count,
            self.ui.dialog_limit,
            self.ui.carousel_index,
            self.ui.carousel_count,
            self.ui.carousel_limit,
            self.ui.sidebar_index,
            self.ui.sidebar_count,
            self.ui.sidebar_limit,
            self.ui.wall_index,
        ]
        for gift_config_input in gift_config_input_list:
            if not gift_config_input.text() or not gift_config_input.text().isdigit():
                return False
        return True

    def switch_mode(self):
        global select_mode_type
        mode = 0 if self.ui.edit_gift_wall_mode.isChecked() else 1
        if select_mode_type == mode:
            return
        # 检查模式下有未保存修改时，切换模式需先确认
        if select_mode_type == 1 and not self.ensure_unsaved_handled():
            self._revert_mode_radio()
            return
        select_mode_type = mode
        self.reset_ui()
        self.set_select_mode()
        # 切换到检查模式时，如果有选中文件，则加载
        if select_mode_type == 1:
            self.load_outputs_xml_file()
        else:
            self.mark_saved_state()

    def switch_server_url(self):
        if self.ui.server_url_1.isChecked():
            urls.BASE_URL = urls.ALIYUN_SERVER_URL
        elif self.ui.server_url_2.isChecked():
            urls.BASE_URL = urls.IJOYSOFT_SERVER_URL
        else:
            urls.BASE_URL = urls.ALIYUN_SERVER_URL
        json_pro.put_selected_server_url(urls.BASE_URL)
        print("选择的服务器 = %s" % urls.BASE_URL)

    def delete_dir(self):
        reply = QMessageBox.question(
            self, '清空Outputs', '确定清空Outputs吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            utils.delete_dir(path_pro.get_outputs())
            self.check_language.set_radio_button_color()
            self.load_outputs_xml_file()
            QMessageBox.information(self, '提示', 'Outputs已清空!')

    def reset_ui(self, confirm=False):
        if confirm:
            reply = QMessageBox.question(
                self, '重置界面', '确认重置界面吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
            if reply == QMessageBox.No:
                return
        self.edit_language.ui.file_name.setText("")
        self.edit_language.ui.language.setText("")
        add_gift_item_list.clear()
        global add_gift_config_list
        add_gift_config_list = deepcopy(DEFAULT_GIFT_CONFIG_LIST)
        self.content.set_table_widget()
        self.set_gift_config_view()
        self.mark_saved_state()

    def show_progress_dialog(self, title="为便捷而生", message="正在下载，请稍等..."):
        self.progress_dialog.setWindowTitle(title)
        self.progress_dialog.setWindowIcon(icon.get_logo())
        self.progress_dialog.label.setText(message)
        self.progress_dialog.progressBar.setProperty("value", 0)
        self.progress_dialog.show()

    def hide_progress_dialog(self):
        self.progress_dialog.hide()

    # 下载弹框进度条更新UI
    def progress_callback(self, value):
        if self.progress_dialog:
            # print("正在刷新下载进度条 线程名称 = %s" % threading.currentThread().name)
            self.progress_dialog.progressBar.setProperty("value", value["value"])
            if value["value"] == 100:
                # 配置表下载完成
                if value["type"] == "config":
                    if value["success"]:
                        print("配置表下载完成 线程名称 = %s 时间 = %f" %
                              (threading.currentThread().name, time.time() - self.download_start_time))
                        json_pro.put_config_download_time(time.time())
                        download.analysis_gift_data()
                        download.DownloadIcon(self)
                    else:
                        self.hide_progress_dialog()
                        # 开始下载之前下载失败的文件
                        DownloadConfig(self, value["error_list"])

                # 图标下载完成
                if value["type"] == "icon":
                    self.hide_progress_dialog()
                    if value["success"]:
                        print("图标下载完成 线程名称 = %s 时间 = %f" %
                              (threading.currentThread().name, time.time() - self.download_start_time))
                    json_pro.put_icon_download_time(time.time())

    def show_add_gift_wall_dialog(self):
        dialog = QAddGiftDialog(self, add_gift_item_list=add_gift_item_list)
        dialog.setWindowTitle("添加GiftWall")
        dialog.setWindowIcon(icon.get_logo())
        rect = self.frameGeometry()
        x = rect.right() - dialog.width() - 10
        title_bar_height = dialog.style().pixelMetric(QStyle.PM_TitleBarHeight)
        y = int((rect.top() + rect.bottom() - dialog.height() - title_bar_height) / 2)
        dialog.move(x, y)
        dialog.set_add_single_gift_callback(callback=self.add_single_gift_callback)
        dialog.set_add_multiple_gift_callback(callback=self.add_multiple_gift_callback)
        dialog.set_modify_gift_callback(callback=lambda: self.content.set_table_widget())
        dialog.exec()

    def add_multiple_gift_callback(self, entity_list, file_names, languages):
        if not entity_list or not file_names or not languages:
            return
        if not self.get_gift_config_list():
            QMessageBox.information(self, '提示', 'GiftWall配置输入不正确!')
            return

        current_file = (self.edit_language.ui.file_name.text() or "").strip()
        current_languages = [
            part.strip() for part in (self.edit_language.ui.language.text() or "").split(",") if part.strip()
        ]
        current_in_targets = (
            current_file in file_names
            and any(language in languages for language in current_languages)
        )
        # 当前列表在目标中且有未保存修改时，先保存再追加，避免覆盖未保存内容
        if current_in_targets and self.has_unsaved_changes():
            if not self.save_gift_wall_file(show_tip=False):
                return

        xml_pro.append_gift_wall_files(file_names, languages, add_gift_config_list, entity_list)
        self.check_language.set_radio_button_color()

        added_count = 0
        for entity_ in entity_list:
            if utils.is_entity_added(entity_, add_gift_item_list):
                continue
            new_entity = deepcopy(entity_)
            new_entity.show_target = None
            add_gift_item_list.append(new_entity)
            self.add_single_gift_callback(new_entity)
            added_count += 1

        if current_in_targets:
            self.mark_saved_state()
        QMessageBox.information(
            self, '提示',
            '已导出到所选文件\n主列表新增 %d 条（已存在的已跳过）' % added_count)

    def load_signal_xml_file(self, path, tip_enable=True):
        if path:
            gift_entity = xml_pro.analysis_gift_xml(path)
            global add_gift_item_list
            global add_gift_config_list
            add_gift_item_list.clear()
            add_gift_config_list = deepcopy(DEFAULT_GIFT_CONFIG_LIST)
            if download.overall_gift_entity and download.overall_gift_entity.item_list:
                if gift_entity:
                    if gift_entity.item_list:
                        for item1 in gift_entity.item_list:
                            for item2 in download.overall_gift_entity.item_list:
                                if utils.compare_entity(item1, item2):
                                    item = deepcopy(item2)
                                    item.show_target = item1.show_target
                                    add_gift_item_list.append(item)
                                    break
                    if gift_entity.config_list:
                        add_gift_config_list = deepcopy(gift_entity.config_list)
                    self.content.set_table_widget()
                    self.set_gift_config_view()
                else:
                    self.content.set_table_widget()
                    self.set_gift_config_view()
                    if tip_enable:
                        QMessageBox.information(self, '提示', '加载GiftWall失败\n1.文件不存在\n2.解析失败\n3.空白文件')
            else:
                self.content.set_table_widget()
                self.set_gift_config_view()
                QMessageBox.information(self, '提示', '总表数据为空!')
            self.mark_saved_state()

    def load_outputs_xml_file(self):
        if select_mode_type == 1:
            name = self.edit_language.ui.file_name.text()
            language = self.edit_language.ui.language.text()
            if name and language:
                path = path_pro.get_outputs() + \
                       (language if urls.LANGUAGE_LIST[0] != language else "") + "\\" + name
                self.load_signal_xml_file(path, tip_enable=False)

    def add_single_gift_callback(self, entity_):
        index = len(add_gift_item_list) - 1
        self.content.ui.tableWidget.setRowCount(len(add_gift_item_list))
        self.content.set_table_widget_item(index, entity_)
        self.content.ui.tableWidget.selectRow(index)


class QKevinTableWidget(QWidget):
    def __init__(self, parent: QEditGiftWidget = None):
        super(QKevinTableWidget, self).__init__(parent)
        self.ui = table_widget_ui.Ui_Form()
        self.ui.setupUi(self)
        self.__view = parent

        self.__init_table_widget()
        self.ui.tableWidget.keyPressEvent = self.__key_press_event
        self.ui.tableWidget.itemClicked.connect(self.__table_widget_item_click)
        self.ui.tableWidget.itemDoubleClicked.connect(self.__table_widget_item_double_click)

    def __init_table_widget(self):
        self.ui.tableWidget.setSelectionMode(QAbstractItemView.ExtendedSelection)
        self.ui.tableWidget.setSelectionBehavior(QAbstractItemView.SelectRows)

        self.ui.tableWidget.setColumnCount(8)
        self.ui.tableWidget.setHorizontalHeaderLabels(
            ['序号', '图标', '项目名', '产品名 类型', '包名', 'showTarget', '推广图', '操作'])
        self.ui.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.ui.tableWidget.setIconSize(QSize(48, 48))
        self.ui.tableWidget.setColumnWidth(0, 60)
        self.ui.tableWidget.setColumnWidth(1, 60)
        self.ui.tableWidget.setColumnWidth(2, 200)
        self.ui.tableWidget.setColumnWidth(3, 200)
        self.ui.tableWidget.setColumnWidth(4, 270)
        self.ui.tableWidget.setColumnWidth(5, 120)
        self.ui.tableWidget.setColumnWidth(6, 60)
        self.ui.tableWidget.setColumnWidth(7, 80)

    def set_table_widget(self):
        if add_gift_item_list:
            self.ui.tableWidget.setRowCount(len(add_gift_item_list))
            for i in range(len(add_gift_item_list)):
                self.set_table_widget_item(i, add_gift_item_list[i])
        else:
            self.ui.tableWidget.setRowCount(0)

    def set_table_widget_item(self, index, entity_):
        self.ui.tableWidget.setRowHeight(index, 50)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 18))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        entity_.id = str(index + 1)
        item.setText(entity_.id)
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.setItem(index, 0, item)

        item = QTableWidgetItem()
        icon_ = QIcon(path_pro.get_download() + entity_.icon_image_path)
        item.setIcon(icon_)
        self.ui.tableWidget.setItem(index, 1, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 12))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(entity_.project_name)
        self.ui.tableWidget.setItem(index, 2, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 8))
        item.setText("产品名: " + (entity_.title if entity_.title else "") +
                     "\n类   型: " + (entity_.app_type if entity_.app_type else ""))
        self.ui.tableWidget.setItem(index, 3, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 8))
        item.setText(entity_.package_name)
        self.ui.tableWidget.setItem(index, 4, item)

        item = QTableWidgetItem()
        item.setFont(QFont('微软雅黑', 10))
        item.setForeground(QBrush(QColor(57, 61, 255)))
        item.setText(entity_.show_target if entity_.show_target else "")
        item.setTextAlignment(Qt.AlignCenter)
        self.ui.tableWidget.setItem(index, 5, item)

        item = None
        if entity_.poster_path:
            item = QTableWidgetItem()
            icon_ = QIcon(path_pro.get_download() + entity_.poster_path)
            item.setIcon(QIcon(icon_))
        self.ui.tableWidget.setItem(index, 6, item)

        delete_button = QPushButton("删除")
        delete_button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        delete_button.setStyleSheet(
            "background-color: rgb(220, 53, 69);\n"
            "color: rgb(255, 255, 255);\n"
            "font: 9pt \"微软雅黑\";")
        delete_button.clicked.connect(lambda checked=False, row=index: self.__delete_row(row))
        delete_widget = QWidget()
        delete_layout = QHBoxLayout(delete_widget)
        delete_layout.setContentsMargins(4, 8, 4, 8)
        delete_layout.setSpacing(0)
        delete_layout.addWidget(delete_button)
        self.ui.tableWidget.setCellWidget(index, 7, delete_widget)

    def __delete_row(self, row):
        if not (0 <= row < len(add_gift_item_list)):
            return
        add_gift_item_list.pop(row)
        self.set_table_widget()
        self.ui.tableWidget.clearSelection()

    def __table_widget_item_click(self):
        current_item = self.ui.tableWidget.currentItem()
        if not current_item:
            return
        row = current_item.row()
        if not (0 <= row < len(add_gift_item_list)):
            return
        entity_ = add_gift_item_list[row]
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
        elif column == 5:
            QShowTargetDialog(self.__view, row)
        elif column == 6:
            self.__show_poster_dialog(entity_)

    def __show_poster_dialog(self, entity_):
        if not entity_ or not entity_.poster_path:
            return
        dialog = QSeeImageDialog(self.__view)
        if entity_.icon_image_path:
            icon_pixmap = QPixmap(path_pro.get_download() + entity_.icon_image_path)
            dialog.icon.setPixmap(
                icon_pixmap.scaled(dialog.icon.size(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        poster_pixmap = QPixmap(path_pro.get_download() + entity_.poster_path)
        dialog.poster.setPixmap(
            poster_pixmap.scaled(dialog.poster.maximumSize(), Qt.KeepAspectRatio, Qt.SmoothTransformation))
        dialog.setWindowTitle("推广图")
        dialog.exec_()

    def __table_widget_item_double_click(self):
        row = self.ui.tableWidget.currentItem().row()
        package_name = add_gift_item_list[row].package_name
        if not package_name:
            return
        url = "https://play.google.com/store/apps/details?id=" + package_name
        QDesktopServices.openUrl(QUrl(url))

    def __key_press_event(self, event):
        if event.key() == QtCore.Qt.Key_Delete or event.key() == QtCore.Qt.Key_D:
            selected_rows = sorted(
                {item.row() for item in self.ui.tableWidget.selectedItems()}, reverse=True)
            for row in selected_rows:
                if 0 <= row < len(add_gift_item_list):
                    add_gift_item_list.pop(row)
            if selected_rows:
                self.set_table_widget()
                self.ui.tableWidget.clearSelection()
        elif event.key() == QtCore.Qt.Key_Up:
            self.__move_table_widget_item(True)
        elif event.key() == QtCore.Qt.Key_Down:
            self.__move_table_widget_item(False)
        elif event.modifiers() == Qt.ControlModifier and event.key() == Qt.Key_A:
            self.ui.tableWidget.selectAll()
        else:
            super().keyPressEvent(event)

    def __move_table_widget_item(self, up):
        selected_rows = []
        for item in self.ui.tableWidget.selectedItems():
            if item.row() not in selected_rows:
                selected_rows.append(item.row())
        if len(selected_rows) == 1:
            row = selected_rows[0]
            new_row = max(selected_rows[0] - 1, 0) if up else min(row + 1, len(add_gift_item_list) - 1)
            entity_ = add_gift_item_list[row]
            add_gift_item_list.remove(entity_)
            add_gift_item_list.insert(new_row, entity_)
            self.set_table_widget_item(row, add_gift_item_list[row])
            self.set_table_widget_item(new_row, add_gift_item_list[new_row])
            self.ui.tableWidget.selectRow(new_row)


class QEditLanguage(QWidget):
    def __init__(self, parent: QEditGiftWidget = None):
        super(QEditLanguage, self).__init__(parent)
        self.ui = edit_language_ui.Ui_Form()
        self.ui.setupUi(self)
        self.__view = parent

        self.ui.pushButton.clicked.connect(
            lambda: QOutFileDialog(self.__view, urls.XML_NAME_LIST))
        self.ui.pushButton_2.clicked.connect(lambda: QLanguageDialog(self.__view))

    def show(self):
        self.setVisible(True)

    def hide(self):
        self.setVisible(False)


class QCheckLanguage(QWidget):
    def __init__(self, parent: QEditGiftWidget = None):
        super(QCheckLanguage, self).__init__(parent)
        self.ui = check_language_ui.Ui_Form()
        self.ui.setupUi(self)
        self.__view = parent

        self.file_name_radio_list = [
            self.ui.file_name_radio_1,
            self.ui.file_name_radio_2,
            self.ui.file_name_radio_3,
            self.ui.file_name_radio_4,
            self.ui.file_name_radio_5,
            self.ui.file_name_radio_6,
            self.ui.file_name_radio_7,
            self.ui.file_name_radio_8,
            self.ui.file_name_radio_9,
            self.ui.file_name_radio_10,
            self.ui.file_name_radio_11,
            self.ui.file_name_radio_12,
            self.ui.file_name_radio_13,
            self.ui.file_name_radio_14,
            self.ui.file_name_radio_15,
            self.ui.file_name_radio_16,
            self.ui.file_name_radio_17,
            self.ui.file_name_radio_18,
        ]
        self.language_radio_list = [
            self.ui.language_radio_1,
            self.ui.language_radio_3,
            self.ui.language_radio_5,
            self.ui.language_radio_7,
            self.ui.language_radio_9,
            self.ui.language_radio_11,
            self.ui.language_radio_2,
            self.ui.language_radio_4,
            self.ui.language_radio_6,
            self.ui.language_radio_8,
            self.ui.language_radio_10,
            self.ui.language_radio_12,
        ]

        self.__init_radio_button(self.__view.edit_language.ui.file_name, self.file_name_radio_list, urls.XML_NAME_LIST)
        self.__init_radio_button(self.__view.edit_language.ui.language, self.language_radio_list, urls.LANGUAGE_LIST)

    def __init_radio_button(self, label, radio_list, string_list):
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(radio_list)):
            if i < len(string_list) and string_list[i]:
                utils.set_radio_button_style_8pt(radio_list[i], False)
                radio_list[i].setText(_translate("Form", string_list[i]))
                if radio_list[i].isChecked():
                    label.setText(radio_list[i].text())
                radio_list[i].toggled.connect(
                    lambda: self.__radio_button_click(label, radio_list))
            else:
                # 隐藏无配置或多余的按钮
                radio_list[i].setText("")
                radio_list[i].hide()

    def __restore_radio_selection(self, label, radio_button_list):
        for radio_button in radio_button_list:
            radio_button.blockSignals(True)
        for radio_button in radio_button_list:
            radio_button.setChecked(radio_button.text() == label.text())
        for radio_button in radio_button_list:
            radio_button.blockSignals(False)

    def __radio_button_click(self, label, radio_button_list):
        new_text = None
        if radio_button_list:
            for radio_button in radio_button_list:
                if radio_button.isChecked():
                    new_text = radio_button.text()
                    break
        if not new_text or label.text() == new_text:
            return

        global select_mode_type
        if select_mode_type == 1 and self.__view.has_unsaved_changes():
            if not self.__view.ensure_unsaved_handled():
                self.__restore_radio_selection(label, radio_button_list)
                return

        label.setText(new_text)
        self.set_radio_button_color()
        # 检查模式时，选取了文件名或者地区后，加载对应的配置文件
        if select_mode_type == 1:
            self.__view.load_outputs_xml_file()

    def set_radio_button_color(self):
        outputs_dir_list = utils.get_outputs_dir_list()
        for radio in self.language_radio_list:
            if not radio.text():
                continue
            utils.set_radio_button_style_8pt(radio, radio.text() not in outputs_dir_list)
        for radio in self.file_name_radio_list:
            if not radio.text():
                continue
            language = self.__view.edit_language.ui.language.text()
            dir_name = language if language != urls.LANGUAGE_LIST[0] else ""
            utils.set_radio_button_style_8pt(
                radio, language and not os.path.exists(path_pro.get_outputs() + dir_name + "\\" + radio.text()))

    def show(self):
        self.setVisible(True)

        for radio in self.language_radio_list:
            if radio.isChecked():
                self.__view.edit_language.ui.language.setText(radio.text())
        for radio in self.file_name_radio_list:
            if radio.isChecked():
                self.__view.edit_language.ui.file_name.setText(radio.text())
        self.set_radio_button_color()

    def hide(self):
        self.setVisible(False)


class QEditOperation(QWidget):
    def __init__(self, parent: QEditGiftWidget = None):
        super(QEditOperation, self).__init__(parent)
        self.ui = edit_button_ui.Ui_Form()
        self.ui.setupUi(self)
        self.__view = parent
        self.setMinimumSize(400, 160)

        self.ui.reload_data_config.clicked.connect(self.__reload_data_config)
        self.ui.reload_data.clicked.connect(self.__reload_data)
        self.ui.reset_ui.clicked.connect(lambda: self.__view.reset_ui(confirm=True))

        self.ui.add_gift_wall.clicked.connect(self.__view.show_add_gift_wall_dialog)
        self.ui.import_gift_wall.clicked.connect(self.__import_gift_wall)
        self.ui.create_gift_wall_file.clicked.connect(self.__save_gift_wall_file)

        self.ui.open_outputs.clicked.connect(lambda: os.system("start " + path_pro.get_outputs()))
        self.ui.clear_outputs.clicked.connect(self.__view.delete_dir)

    def __reload_data_config(self):
        reply = QMessageBox.question(
            self.__view, '重新下载', '确认重新下载服务器配置表吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            json_pro.put_config_download_time(0)
            download.init_gift_data(self.__view)

    def __reload_data(self):
        reply = QMessageBox.question(
            self.__view, '重新下载', '确认重新下载服务器数据吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            json_pro.put_config_download_time(0)
            json_pro.put_icon_download_time(0)
            download.init_gift_data(self.__view)

    def __import_gift_wall(self):
        file_name, file_type = QFileDialog.getOpenFileName(self.__view, "选取文件", path_pro.get_outputs())
        self.__view.load_signal_xml_file(file_name)

    def __save_gift_wall_file(self):
        reply = QMessageBox.question(
            self.__view, '生成GiftWall配置表', '确定生成GiftWall配置表吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.__view.save_gift_wall_file()


class QCheckOperation(QWidget):
    def __init__(self, parent: QEditGiftWidget = None):
        super(QCheckOperation, self).__init__(parent)
        self.ui = check_button_ui.Ui_Form()
        self.ui.setupUi(self)
        self.__view = parent
        self.setMinimumSize(400, 110)

        self.ui.open_outputs_2.clicked.connect(lambda: os.system("start " + path_pro.get_outputs()))
        self.ui.clear_outputs_2.clicked.connect(self.__view.delete_dir)

        self.ui.save.clicked.connect(self.__view.save_gift_wall_file)
        self.ui.add_gift_wall_2.clicked.connect(self.__view.show_add_gift_wall_dialog)
        self.ui.cancel_save.clicked.connect(self.__cancel_save)

    def __cancel_save(self):
        reply = QMessageBox.question(
            self.__view, '放弃修改', '确定放弃修改吗?', QMessageBox.No | QMessageBox.Yes, QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.__view.load_outputs_xml_file()


class QShowTargetDialog:
    def __init__(self, view_: QEditGiftWidget, row):
        self.__view = view_
        self.__row = row
        if not (0 <= row < len(add_gift_item_list)):
            return
        show_target_list = xml_pro.SHOW_TARGET_LIST
        if not show_target_list:
            QMessageBox.information(self.__view, '提示', '未配置showTarget可选值!')
            return

        dialog = QSingleSelectDialog(self.__view)
        dialog.setWindowTitle("选择showTarget")
        dialog.setWindowIcon(icon.get_logo())

        radio_button_list = [
            dialog.radioButton,
            dialog.radioButton_2,
            dialog.radioButton_3,
            dialog.radioButton_4,
            dialog.radioButton_5,
            dialog.radioButton_6,
            dialog.radioButton_7,
            dialog.radioButton_8,
            dialog.radioButton_9,
            dialog.radioButton_10,
            dialog.radioButton_11,
            dialog.radioButton_12,
            dialog.radioButton_13,
            dialog.radioButton_14,
            dialog.radioButton_15,
            dialog.radioButton_16,
            dialog.radioButton_17,
            dialog.radioButton_18,
        ]
        current_show_target = add_gift_item_list[row].show_target or ""
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(show_target_list)):
            if i >= len(radio_button_list):
                break
            utils.set_radio_button_style_10pt(radio_button_list[i], False)
            display_text = "空" if show_target_list[i] == "" else show_target_list[i]
            radio_button_list[i].setText(_translate("Form", display_text))
            radio_button_list[i].setChecked(current_show_target == show_target_list[i])
            radio_button_list[i].toggled.connect(
                lambda: self.__set_show_target(dialog, radio_button_list, show_target_list))
        for i in range(len(radio_button_list)):
            if i >= len(show_target_list):
                radio_button_list[i].hide()
        dialog.exec()

    def __set_show_target(self, dialog, radio_button_list, show_target_list):
        if not (0 <= self.__row < len(add_gift_item_list)):
            return
        for i, radio_button in enumerate(radio_button_list):
            if i >= len(show_target_list):
                break
            if radio_button.isChecked():
                show_target = show_target_list[i] or None
                if (add_gift_item_list[self.__row].show_target or None) == show_target:
                    return
                add_gift_item_list[self.__row].show_target = show_target
                self.__view.content.set_table_widget_item(self.__row, add_gift_item_list[self.__row])
                self.__view.content.ui.tableWidget.selectRow(self.__row)
                dialog.hide()
                return


class QOutFileDialog:
    def __init__(self, view_: QEditGiftWidget, string_list):
        self.__view = view_
        string_list_modify = []
        for name in string_list:
            if not name:
                continue
            string_list_modify.append(name)

        out_file_dialog = QSingleSelectDialog(self.__view)
        out_file_dialog.setWindowTitle("选择字符")
        out_file_dialog.setWindowIcon(icon.get_logo())

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
            out_file_dialog.radioButton_16,
            out_file_dialog.radioButton_17,
            out_file_dialog.radioButton_18,
        ]
        # 设置按钮状态和点击事件
        _translate = QtCore.QCoreApplication.translate
        for i in range(len(string_list_modify)):
            utils.set_radio_button_style_10pt(out_file_radio_button_list[i], False)
            out_file_radio_button_list[i].setText(_translate("Form", string_list_modify[i]))
            out_file_radio_button_list[i].setChecked(
                self.__view.edit_language.ui.file_name.text() == string_list_modify[i])
            out_file_radio_button_list[i].toggled.connect(
                lambda: self.__set_out_file(out_file_dialog, out_file_radio_button_list))
        # 隐藏多出来的按钮
        if len(out_file_radio_button_list) > len(string_list_modify):
            for i in range(len(out_file_radio_button_list)):
                if i >= len(string_list_modify):
                    out_file_radio_button_list[i].hide()
        out_file_dialog.exec()

    def __set_out_file(self, out_file_dialog, out_file_radio_button_list):
        if out_file_radio_button_list:
            for radio_button in out_file_radio_button_list:
                if radio_button.isChecked():
                    if self.__view.edit_language.ui.file_name.text() == radio_button.text():
                        return
                    self.__view.edit_language.ui.file_name.setText(radio_button.text())
                    out_file_dialog.hide()


class QLanguageDialog:
    def __init__(self, view_: QEditGiftWidget):
        self.__view = view_

        language_dialog = QMultipleSelectDialog(self.__view)
        language_dialog.setWindowTitle("选择地区")
        language_dialog.setWindowIcon(icon.get_logo())

        self.language_check_box_list = [
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
            utils.set_check_box_style(self.language_check_box_list[i])
            self.language_check_box_list[i].setText(_translate("Dialog", urls.LANGUAGE_LIST[i].ljust(50, " ")))
            self.language_check_box_list[i].setChecked(
                urls.LANGUAGE_LIST[i] in self.__view.edit_language.ui.language.text())
            self.language_check_box_list[i].toggled.connect(
                lambda: self.__select_language(self.language_check_box_list))
        # 隐藏多出来的按钮
        if len(self.language_check_box_list) > len(urls.LANGUAGE_LIST):
            for i in range(len(self.language_check_box_list)):
                if i >= len(urls.LANGUAGE_LIST):
                    self.language_check_box_list[i].hide()
        language_dialog.deselect_all.clicked.connect(lambda: self.__select_all_language(False))
        language_dialog.select_all.clicked.connect(lambda: self.__select_all_language(True))
        language_dialog.ok.clicked.connect(lambda: language_dialog.hide())
        language_dialog.exec()

    def __select_language(self, language_check_box_list):
        if language_check_box_list:
            self.__view.edit_language.ui.language.setText("")
            for radio_button in language_check_box_list:
                if radio_button.isChecked():
                    self.__view.edit_language.ui.language.setText(
                        self.__view.edit_language.ui.language.text() + radio_button.text().strip(" ") + ",")

    def __select_all_language(self, enable):
        for i in range(len(urls.LANGUAGE_LIST)):
            self.language_check_box_list[i].setChecked(enable)
