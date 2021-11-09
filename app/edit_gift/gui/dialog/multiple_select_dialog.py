from PyQt5.QtWidgets import QDialog

from app.edit_gift.gui.dialog import multiple_select_ui


class QMultipleSelectDialog(QDialog, multiple_select_ui.Ui_Dialog):
    def __init__(self, parent=None):
        super(QMultipleSelectDialog, self).__init__(parent)
        self.setupUi(self)
