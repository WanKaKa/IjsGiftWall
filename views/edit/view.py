from PyQt5.QtCore import QSize
from PyQt5.QtGui import QIcon, QFont, QBrush, QColor
from PyQt5.QtWidgets import QWidget, QAbstractItemView, QTableWidgetItem

from utils import path_utils
from views.edit import edit_gift_ui
import giftdata
from giftdata import urls


class View(QWidget, edit_gift_ui.Ui_Form):
    def __init__(self, parent=None):
        super(View, self).__init__(parent)
        self.setupUi(self)

    def init_view(self):
        if giftdata.overall_gift_entity:
            overall_gift_entity = giftdata.overall_gift_entity
            self.tableWidget.setRowCount(len(overall_gift_entity.item_list))
            self.tableWidget.setColumnCount(7)
            self.tableWidget.setHorizontalHeaderLabels(['Icon', '项目名', '产品名', '类型', '包名', '推广图', '操作'])
            self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)
            self.tableWidget.setIconSize(QSize(64, 64))
            self.tableWidget.setColumnWidth(0, 80)
            self.tableWidget.setColumnWidth(1, 240)
            self.tableWidget.setColumnWidth(2, 180)
            self.tableWidget.setColumnWidth(3, 180)
            self.tableWidget.setColumnWidth(4, 300)
            self.tableWidget.setColumnWidth(5, 80)
            self.tableWidget.setColumnWidth(6, 80)
            for i in range(len(overall_gift_entity.item_list)):
                self.tableWidget.setRowHeight(i, 80)

            for i in range(len(overall_gift_entity.item_list)):
                item = QTableWidgetItem()
                icon = QIcon(path_utils.get_download_path() + overall_gift_entity.item_list[i].icon_image_path)
                item.setIcon(QIcon(icon))
                self.tableWidget.setItem(i, 0, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 12))
                item.setForeground(QBrush(QColor(85, 85, 255)))
                item.setText(overall_gift_entity.item_list[i].project_name)
                self.tableWidget.setItem(i, 1, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 10))
                item.setText(overall_gift_entity.item_list[i].title)
                self.tableWidget.setItem(i, 2, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 10))
                item.setText(overall_gift_entity.item_list[i].app_type)
                self.tableWidget.setItem(i, 3, item)

                item = QTableWidgetItem()
                item.setFont(QFont('微软雅黑', 8))
                item.setText(overall_gift_entity.item_list[i].package_name)
                self.tableWidget.setItem(i, 4, item)

                if overall_gift_entity.item_list[i].poster_path:
                    item = QTableWidgetItem()
                    icon = QIcon(path_utils.get_download_path() + overall_gift_entity.item_list[i].poster_path)
                    item.setIcon(QIcon(icon))
                    self.tableWidget.setItem(i, 5, item)
