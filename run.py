import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

import gift.download
import gui.main.view
import util.utils

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    view_ = gui.main.view.EditGiftView()
    view_.show()

    # 初始化服务器GiftWall数据
    gift.download.init_gift_data(view_)
    view_.init_view()

    # 拷贝资源（图片资源放在exe文件中读取不到）
    util.utils.copy_res()
    sys.exit(app.exec_())
