from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget

import gift.download
from gui.main.edit_gift import EditGiftView
from util import icon

import gui.main.main_window_ui


class QKevinMainWindow(QWidget):
    def __init__(self, parent=None):
        super(QKevinMainWindow, self).__init__(parent)
        self.__ui = gui.main.main_window_ui.Ui_From()
        self.__ui.setupUi(self)

        self.setWindowTitle("广告配置编辑-为便捷而生")
        self.setWindowIcon(icon.get_logo())
        self.setWindowState(Qt.WindowMaximized)

        self.__edit_gift = EditGiftView()
        self.__ui.content.addWidget(self.__edit_gift)

        # 初始化服务器GiftWall数据
        gift.download.init_gift_data(self.__edit_gift)
        self.__edit_gift.init_view()
