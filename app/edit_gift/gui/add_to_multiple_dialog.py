from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QDialog, QVBoxLayout, QHBoxLayout, QLabel, QCheckBox, QPushButton,
    QScrollArea, QWidget, QFrame
)

from app.edit_gift.core import urls
from util import utils


class QAddToMultipleDialog(QDialog):
    """选择多个文件名和地区后添加。"""

    def __init__(self, parent=None, default_file_names=None, default_languages=None):
        super(QAddToMultipleDialog, self).__init__(parent)
        self.setWindowTitle("添加到多个列表")
        self.setMinimumSize(560, 640)
        self.resize(560, 720)
        self.setStyleSheet("background-color: rgb(255, 255, 255);")

        self.__file_name_list = [name for name in urls.XML_NAME_LIST if name]
        self.__language_list = list(urls.LANGUAGE_LIST)
        self.__default_file_names = set(default_file_names or [])
        self.__default_languages = set(default_languages or [])
        self.__file_check_boxes = []
        self.__language_check_boxes = []

        self.__init_ui()

    def __init_ui(self):
        root = QVBoxLayout(self)
        root.setContentsMargins(12, 12, 12, 12)
        root.setSpacing(10)

        columns = QHBoxLayout()
        columns.setSpacing(16)

        file_column = self.__build_check_column(
            "文件名", self.__file_name_list, self.__default_file_names, self.__file_check_boxes)
        language_column = self.__build_check_column(
            "地区", self.__language_list, self.__default_languages, self.__language_check_boxes)
        columns.addWidget(file_column, 1)
        columns.addWidget(language_column, 1)
        root.addLayout(columns, 1)

        bottom = QHBoxLayout()
        bottom.addStretch(1)
        add_button = QPushButton("添加")
        add_button.setFixedSize(120, 40)
        add_button.setStyleSheet(
            "background-color: rgb(57, 61, 255); color: rgb(255, 255, 255); font: 12pt \"微软雅黑\";")
        add_button.clicked.connect(self.accept)
        bottom.addWidget(add_button)
        root.addLayout(bottom)

    def __build_check_column(self, title, options, defaults, check_box_list):
        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        layout = QVBoxLayout(frame)
        layout.setContentsMargins(8, 8, 8, 8)
        layout.setSpacing(6)

        title_label = QLabel(title)
        title_label.setStyleSheet("font: 12pt \"微软雅黑\"; color: rgb(57, 61, 255);")
        layout.addWidget(title_label)

        tool_row = QHBoxLayout()
        select_all = QPushButton("全选")
        deselect_all = QPushButton("取消全选")
        for btn in (select_all, deselect_all):
            btn.setFixedHeight(32)
            btn.setStyleSheet(
                "background-color: rgb(57, 61, 255); color: rgb(255, 255, 255); font: 10pt \"微软雅黑\";")
        tool_row.addWidget(deselect_all)
        tool_row.addWidget(select_all)
        layout.addLayout(tool_row)

        scroll = QScrollArea()
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        content = QWidget()
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(4, 4, 4, 4)
        content_layout.setSpacing(4)

        for name in options:
            check_box = QCheckBox(name)
            utils.set_check_box_style(check_box)
            check_box.setChecked(name in defaults)
            content_layout.addWidget(check_box)
            check_box_list.append(check_box)

        content_layout.addStretch(1)
        scroll.setWidget(content)
        layout.addWidget(scroll, 1)

        select_all.clicked.connect(lambda: self.__set_all_checked(check_box_list, True))
        deselect_all.clicked.connect(lambda: self.__set_all_checked(check_box_list, False))
        return frame

    @staticmethod
    def __set_all_checked(check_box_list, checked):
        for check_box in check_box_list:
            check_box.setChecked(checked)

    def get_selected_file_names(self):
        return [cb.text().strip() for cb in self.__file_check_boxes if cb.isChecked()]

    def get_selected_languages(self):
        return [cb.text().strip() for cb in self.__language_check_boxes if cb.isChecked()]
