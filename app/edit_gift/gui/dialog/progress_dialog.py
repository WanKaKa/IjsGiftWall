from PyQt5.QtWidgets import QDialog

from app.edit_gift.gui.dialog import progress_ui


class QProgressDialog(QDialog, progress_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(QProgressDialog, self).__init__(parent)
        self.setupUi(self)
