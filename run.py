import sys

from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt

import util.utils
from gui.main.main_window_widget import QKevinMainWindow

if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    app = QApplication(sys.argv)

    main_window = QKevinMainWindow()
    main_window.show()

    # 拷贝资源(图片资源放在exe文件中读取不到)
    util.utils.copy_res()
    sys.exit(app.exec_())
