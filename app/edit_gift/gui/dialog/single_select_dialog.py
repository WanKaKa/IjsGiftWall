from PyQt5.QtWidgets import QDialog

from app.edit_gift.gui.dialog import single_select_ui


class QSingleSelectDialog(QDialog, single_select_ui.Ui_Form):
    def __init__(self, parent=None):
        super(QSingleSelectDialog, self).__init__(parent)
        self.setupUi(self)
