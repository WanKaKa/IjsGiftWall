from PyQt5 import QtCore

import gui.dialog
from util import icon


def show_dialog(view_, string_list, label):
    out_file_dialog = gui.dialog.SingleSelectDialog(view_)
    out_file_dialog.setWindowTitle("选择字符-为便捷而生")
    out_file_dialog.setWindowIcon(icon.get_logo())

    out_file_radio_button_list = [
        out_file_dialog.radioButton,
        out_file_dialog.radioButton_2,
        out_file_dialog.radioButton_3,
        out_file_dialog.radioButton_4,
        out_file_dialog.radioButton_5,
        out_file_dialog.radioButton_6,
        out_file_dialog.radioButton_7,
        out_file_dialog.radioButton_8,
        out_file_dialog.radioButton_9,
        out_file_dialog.radioButton_10,
        out_file_dialog.radioButton_11,
        out_file_dialog.radioButton_12,
        out_file_dialog.radioButton_13,
        out_file_dialog.radioButton_14,
        out_file_dialog.radioButton_15,
        out_file_dialog.radioButton_16
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(string_list)):
        out_file_radio_button_list[i].setText(_translate("Form", string_list[i]))
        out_file_radio_button_list[i].setChecked(label.text() == string_list[i])
        out_file_radio_button_list[i].toggled.connect(
            lambda: set_out_file(label, out_file_dialog, out_file_radio_button_list))
    # 隐藏多出来的按钮
    if len(out_file_radio_button_list) > len(string_list):
        for i in range(len(out_file_radio_button_list)):
            if i >= len(string_list):
                out_file_radio_button_list[i].hide()
    out_file_dialog.exec()


def set_out_file(label, out_file_dialog, out_file_radio_button_list):
    if out_file_radio_button_list:
        for radio_button in out_file_radio_button_list:
            if radio_button.isChecked():
                if label.text() == radio_button.text():
                    return
                label.setText(radio_button.text())
                out_file_dialog.hide()
