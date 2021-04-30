from PyQt5 import QtCore

import view.dialog
from gift import urls
from util import icon


def show_dialog(view_):
    language_dialog = view.dialog.MultipleSelectDialog(view_)
    language_dialog.setWindowTitle("选择地区-为便捷而生")
    language_dialog.setWindowIcon(icon.get_logo())

    language_check_box_list = [
        language_dialog.checkBox,
        language_dialog.checkBox_2,
        language_dialog.checkBox_3,
        language_dialog.checkBox_4,
        language_dialog.checkBox_5,
        language_dialog.checkBox_6,
        language_dialog.checkBox_7,
        language_dialog.checkBox_8,
        language_dialog.checkBox_9,
        language_dialog.checkBox_10,
        language_dialog.checkBox_11,
        language_dialog.checkBox_12,
        language_dialog.checkBox_13,
        language_dialog.checkBox_14,
        language_dialog.checkBox_15,
        language_dialog.checkBox_16,
    ]
    # 设置按钮状态和点击事件
    _translate = QtCore.QCoreApplication.translate
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setText(_translate("Dialog", urls.LANGUAGE_LIST[i].ljust(50, " ")))
        language_check_box_list[i].setChecked(urls.LANGUAGE_LIST[i] in view_.language.text())
        language_check_box_list[i].toggled.connect(
            lambda: select_language(view_, language_check_box_list))
    # 隐藏多出来的按钮
    if len(language_check_box_list) > len(urls.LANGUAGE_LIST):
        for i in range(len(language_check_box_list)):
            if i >= len(urls.LANGUAGE_LIST):
                language_check_box_list[i].hide()
    language_dialog.deselect_all.clicked.connect(lambda: select_all_language(language_check_box_list, False))
    language_dialog.select_all.clicked.connect(lambda: select_all_language(language_check_box_list, True))
    language_dialog.ok.clicked.connect(lambda: language_dialog.hide())
    language_dialog.exec()


def select_language(view_, language_check_box_list):
    if language_check_box_list:
        view_.language.setText("")
        for radio_button in language_check_box_list:
            if radio_button.isChecked():
                view_.language.setText(view_.language.text() + radio_button.text().strip(" ") + ",")


def select_all_language(language_check_box_list, enable):
    for i in range(len(urls.LANGUAGE_LIST)):
        language_check_box_list[i].setChecked(enable)
