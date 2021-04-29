import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

import gift.download
import view.edit.view

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    desktop = app.desktop()
    width = desktop.width()
    height = desktop.height()
    view_ = view.edit.view.EditGiftView()
    view_.show()
    view_.move(int((width - view_.width()) / 2), int((height - view_.height()) / 2 - 30))

    # 初始化服务器GiftWall数据
    gift.download.init_gift_data(view_)

    view_.init_view()
    sys.exit(app.exec_())
