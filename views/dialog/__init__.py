from PyQt5.QtWidgets import QDialog

from views.dialog import progress_dialog


class ProgressDialog(QDialog, progress_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi(self)
