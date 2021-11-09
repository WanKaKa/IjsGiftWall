from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QDialog, QApplication

from app.edit_gift.gui.dialog import see_image_ui


class QSeeImageDialog(QDialog, see_image_ui.Ui_Form):
    def __init__(self, parent=None):
        super(QSeeImageDialog, self).__init__(parent)
        self.setupUi(self)
        self.installEventFilter(self)

    def eventFilter(self, o, e):
        if e.type() == QEvent.ActivationChange:
            if QApplication.activeWindow() != self:
                self.hide()
        return QDialog.eventFilter(self, o, e)
