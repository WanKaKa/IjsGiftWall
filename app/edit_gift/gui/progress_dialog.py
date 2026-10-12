from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QDialog

from app.edit_gift.gui.qt5.dialog import progress_ui


class QProgressDialog(QDialog, progress_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(QProgressDialog, self).__init__(parent)
        self.setupUi(self)
        # 保证提示文字完整换行显示，不被截断成省略号
        self.label.setWordWrap(True)
        self.label.setAlignment(Qt.AlignCenter | Qt.AlignVCenter)
        self.label.setTextFormat(Qt.PlainText)
