import sys
import giftdata
from PyQt5.QtWidgets import QApplication
from views import edit

if __name__ == '__main__':
    app = QApplication(sys.argv)
    desktop = app.desktop()
    edit_gift = edit.view.View()
    edit_gift.show()

    # 初始化服务器GiftWall数据
    giftdata.init_gift_data(edit_gift)

    edit_gift.init_view()
    sys.exit(app.exec_())
