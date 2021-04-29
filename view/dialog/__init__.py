from PyQt5.QtCore import QEvent
from PyQt5.QtWidgets import QDialog, QApplication

from view.dialog import progress_dialog
from view.dialog import single_select_dialog
from view.dialog import multiple_select_dialog
from view.dialog import see_image_dialog


class ProgressDialog(QDialog, progress_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(ProgressDialog, self).__init__(parent)
        self.setupUi(self)


class SingleSelectDialog(QDialog, single_select_dialog.Ui_Form):
    def __init__(self, parent=None):
        super(SingleSelectDialog, self).__init__(parent)
        self.setupUi(self)


class MultipleSelectDialog(QDialog, multiple_select_dialog.Ui_Dialog):
    def __init__(self, parent=None):
        super(MultipleSelectDialog, self).__init__(parent)
        self.setupUi(self)


class SeeImageDialog(QDialog, see_image_dialog.Ui_Form):
    def __init__(self, parent=None):
        super(SeeImageDialog, self).__init__(parent)
        self.setupUi(self)
        self.installEventFilter(self)

    def eventFilter(self, o, e):
        if e.type() == QEvent.ActivationChange:
            if QApplication.activeWindow() != self:
                self.hide()
        return QDialog.eventFilter(self, o, e)
