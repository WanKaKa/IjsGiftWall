import sys

from PyQt5.QtCore import QCoreApplication, Qt

from giftdata import download
from PyQt5.QtWidgets import QApplication
from view import edit

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)
    desktop = app.desktop()
    edit_gift_view = edit.view.EditGiftView()
    edit_gift_view.show()

    # 初始化服务器GiftWall数据
    download.init_gift_data(edit_gift_view)

    edit_gift_view.init_view()
    sys.exit(app.exec_())
