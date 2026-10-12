import sys

from util import ui_scale

# 须在创建 QApplication 之前：关闭系统自动缩放（用户比例运行时应用）
ui_scale.apply_scale_env()

from PyQt5.QtWidgets import QApplication, QDialog
from PyQt5.QtCore import QCoreApplication, Qt
from main_window_widget import QKevinMainWindow

import util.utils


def _install_dialog_scale_polish():
    """对话框显示前按当前比例抛光（不子类化 Qt，避免 sip DeprecationWarning）。"""

    def _wrap(method):
        def wrapped(self, *args, **kwargs):
            # WindowType 是枚举值而非独立位标志：不能用 flags & Qt.ToolTip。
            # Dialog(0x3) 与 ToolTip(0xd) 按位与非零，会导致设置等对话框永远跳过抛光，
            # 表现为：滑块仍是已保存的 1.50，但控件几何停在设计稿 1.0。
            if self.windowType() not in (Qt.ToolTip, Qt.Popup, Qt.SplashScreen):
                ui_scale.polish_window(self)
            return method(self, *args, **kwargs)

        return wrapped

    # PyQt5 中 exec 与 exec_ 不是同一函数，两处都要包，否则 dialog.exec() 不会抛光
    QDialog.exec_ = _wrap(QDialog.exec_)
    QDialog.exec = _wrap(QDialog.exec)
    QDialog.open = _wrap(QDialog.open)
    QDialog.show = _wrap(QDialog.show)


if __name__ == '__main__':
    QCoreApplication.setAttribute(Qt.AA_EnableHighDpiScaling)
    QCoreApplication.setAttribute(Qt.AA_UseHighDpiPixmaps)
    app = QApplication(sys.argv)
    _install_dialog_scale_polish()

    main_window = QKevinMainWindow()
    ui_scale.apply_ui_scale(main_window, ui_scale.resolve_scale_factor())
    main_window.refresh_after_ui_scale()
    # 显示前先铺满可用屏幕并标记最大化，避免首帧闪出设计稿尺寸（1400x720）
    screen = app.primaryScreen()
    if screen is not None:
        main_window.setGeometry(screen.availableGeometry())
    main_window.setWindowState(Qt.WindowMaximized)
    main_window.show()

    # 拷贝资源(图片资源放在exe文件中读取不到)
    util.utils.copy_res()
    sys.exit(app.exec_())
