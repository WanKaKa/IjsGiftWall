import sys
import os


def _configure_high_dpi():
    """高分屏适配：不跟随系统 150%/200% 放大，避免字过大、界面显示不全。"""
    # 界面按固定像素设计；固定 100% 布局缩放（可用环境变量 QT_SCALE_FACTOR 覆盖）
    os.environ.setdefault("QT_SCALE_FACTOR", "1")
    os.environ.setdefault("QT_AUTO_SCREEN_SCALE_FACTOR", "0")
    # 字体也不跟随系统缩放（pt 按 96 DPI 计算，与 100% 显示一致）
    os.environ.setdefault("QT_FONT_DPI", "96")


from PyQt5.QtWidgets import QApplication
from PyQt5.QtCore import QCoreApplication, Qt
from main_window_widget import QKevinMainWindow

import util.utils

if __name__ == '__main__':
    _configure_high_dpi()
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)

    main_window = QKevinMainWindow()
    main_window.show()

    # 拷贝资源(图片资源放在exe文件中读取不到)
    util.utils.copy_res()
    sys.exit(app.exec_())
