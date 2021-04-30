import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

import gift.download
import view.main.view

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    view_ = view.main.view.EditGiftView()
    view_.show()

    # 初始化服务器GiftWall数据
    gift.download.init_gift_data(view_)

    view_.init_view()
    sys.exit(app.exec_())
