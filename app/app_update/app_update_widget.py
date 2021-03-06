from PyQt5 import QtCore, QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QMessageBox

from app.app_update import app_update_ui
from app.app_update import app_update_item_ui
import xml.dom.minidom


class ItemInfo:

    def __init__(self):
        self.min_version = None
        self.max_version = None
        self.priority = None


def save_app_update_xml(directory, version, item_list):
    file = open(directory + "\\" + "update_info.xml", mode='w', encoding='utf-8')
    file.write("<?xml version=\"1.0\" encoding=\"UTF-8\"?>")
    file.write("\n")
    file.write("<info version=\"" + version + "\">")
    file.write("\n")

    for index in range(len(item_list)):
        item: QKevinAppUpdateItem = item_list[index]
        if item.ui.min_version.text() and item.ui.max_version.text() and item.ui.priority.text():
            range_str = "    <range"
            range_str += " "
            range_str += "min=\"%s\"" % item.ui.min_version.text()
            range_str += " "
            range_str += "max=\"%s\"" % item.ui.max_version.text()
            range_str += " "
            range_str += "p=\"%s\"" % item.ui.priority.text()
            range_str += "/>"
            file.write(range_str)
            file.write("\n")

    file.write("</info>")
    file.write("\n")
    file.close()


def open_app_update_xml(file_path):
    item_list = []
    dom = xml.dom.minidom.parse(file_path)
    root = dom.documentElement
    latest_version = root.getAttribute("version")
    range_list = root.getElementsByTagName("range")
    for item in range_list:
        info = ItemInfo()
        info.min_version = item.getAttribute("min")
        info.max_version = item.getAttribute("max")
        info.priority = item.getAttribute("p")
        info.tip = item.getAttribute("msg")
        item_list.append(info)
    return latest_version, item_list


class QKevinAppUpdateItem(QWidget):
    def __init__(self, parent=None, index=0):
        super(QKevinAppUpdateItem, self).__init__(parent)
        self.ui = app_update_item_ui.Ui_Form()
        self.ui.setupUi(self)

        self.index = index
        self.ui.pb_add_up.clicked.connect(lambda: self.do_add_item(True))
        self.ui.pb_add_down.clicked.connect(lambda: self.do_add_item(False))
        self.ui.pb_delete.clicked.connect(self.do_delete_item)

    def do_add_item(self, up):
        self.add_item(self.index, up)

    def add_item(self, index, up):
        pass

    def do_delete_item(self):
        self.delete_item(self.index)

    def delete_item(self, index):
        pass


class QKevinAppUpdate(QWidget):
    item_list = []

    def __init__(self, parent: QWidget):
        super(QKevinAppUpdate, self).__init__(parent)
        self.ui = app_update_ui.Ui_Form()
        self.ui.setupUi(self)
        self.setWindowState(Qt.WindowMaximized)

        self.ui.save_to.clicked.connect(self.do_save_to)
        self.ui.open_to.clicked.connect(self.do_open_to)

        self.content_layout = QVBoxLayout()
        self.content_layout.setSpacing(6)
        self.ui.content.setLayout(self.content_layout)

        self.init_scroll_area(6)

    def init_scroll_area(self, count):
        for item in self.item_list:
            self.content_layout.removeWidget(item)
            item.deleteLater()
        self.item_list.clear()

        self.ui.content.setMinimumSize(QtCore.QSize(0, count * 80 + (count + 1) * 6))
        for i in range(count):
            item = QKevinAppUpdateItem(parent=self, index=i)
            item.add_item = self.add_item
            item.delete_item = self.delete_item
            self.item_list.append(item)
            self.content_layout.addWidget(item)

    def add_item(self, index, up):
        for item in self.item_list:
            self.content_layout.removeWidget(item)

        item = QKevinAppUpdateItem(parent=self)
        item.add_item = self.add_item
        item.delete_item = self.delete_item
        # ?????????index???????????????
        self.item_list.insert(index if up else index + 1, item)

        count = len(self.item_list)
        self.ui.content.setMinimumSize(QtCore.QSize(0, count * 80 + (count + 1) * 6))
        for i in range(count):
            item = self.item_list[i]
            item.index = i
            self.content_layout.addWidget(item)

    def delete_item(self, index):
        item = self.item_list[index]
        self.item_list.remove(item)
        self.content_layout.removeWidget(item)
        item.deleteLater()

        count = len(self.item_list)
        self.ui.content.setMinimumSize(QtCore.QSize(0, count * 80 + (count + 1) * 6))
        for i in range(count):
            item = self.item_list[i]
            item.index = i

    def do_save_to(self):
        result = self.check_input_correct()
        if result:
            QMessageBox.information(self, '??????', result)
            return
        directory = QtWidgets.QFileDialog.getExistingDirectory(None, "???????????????")
        if directory:
            save_app_update_xml(directory, self.ui.latest_version.text(), self.item_list)
            QMessageBox.information(self, '??????', '????????????????????????????????????')

    def check_input_correct(self):
        # ?????????????????????????????????100
        if not self.ui.latest_version.text().isdigit() or int(self.ui.latest_version.text()) < 100:
            return "???????????????????????????"
        latest_version = int(self.ui.latest_version.text())
        for index in range(len(self.item_list)):
            item: QKevinAppUpdateItem = self.item_list[index]

            # ?????????????????????????????????????????????????????????100
            if (item.ui.min_version.text() and (not item.ui.min_version.text().isdigit()
                                                or int(item.ui.min_version.text()) < 100
                                                or int(item.ui.min_version.text()) > latest_version)):
                return "??????????????????????????? ?????? = %d" % (index + 1)

            # ?????????????????????????????????????????????????????????100
            if (item.ui.max_version.text() and (not item.ui.max_version.text().isdigit()
                                                or int(item.ui.max_version.text()) < 100
                                                or int(item.ui.max_version.text()) > latest_version)):
                return "??????????????????????????? ?????? = %d" % (index + 1)

            # ??????????????????1???2???3
            if item.ui.priority.text() and item.ui.priority.text() not in ["1", "2", "3"]:
                return "????????????????????? ?????? = %d" % (index + 1)

            # ???????????????????????????????????????????????????????????????????????????
            if item.ui.min_version.text() or item.ui.max_version.text() or item.ui.priority.text():
                if not (item.ui.min_version.text() and item.ui.max_version.text() and item.ui.priority.text()):
                    return "??????????????? ?????? = %d" % (index + 1)

            if item.ui.min_version.text() and item.ui.max_version.text():
                if int(item.ui.min_version.text()) > int(item.ui.max_version.text()):
                    return "??????????????? > ??????????????? ?????? = %d" % (index + 1)

            if index != 0:
                # ????????????????????????????????????????????????
                if item.ui.min_version.text() or item.ui.max_version.text() or item.ui.priority.text():
                    pre_item: QKevinAppUpdateItem = self.item_list[index - 1]
                    if (not pre_item.ui.min_version.text()
                            or not pre_item.ui.max_version.text() or not pre_item.ui.priority.text()):
                        return "??????????????? ?????? = %d" % index
                    if item.ui.min_version.text():
                        if int(item.ui.min_version.text()) <= int(pre_item.ui.max_version.text()):
                            return "??????????????? <= ???????????????(?????????) ?????? = %d" % (index + 1)
        return None

    def do_open_to(self):
        file_path = QtWidgets.QFileDialog.getOpenFileName(self, "????????????", '.', "(*.xml)")
        if file_path[0]:
            result = open_app_update_xml(file_path[0])
            self.ui.latest_version.setText(result[0])
            self.init_scroll_area(len(result[1]) + 4)
            for index in range(len(result[1])):
                info: ItemInfo = result[1][index]
                item: QKevinAppUpdateItem = self.item_list[index]
                item.ui.min_version.setText(info.min_version)
                item.ui.max_version.setText(info.max_version)
                item.ui.priority.setText(info.priority)
