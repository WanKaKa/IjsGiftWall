# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'app_update_item_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1280, 80)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(0, 0, 1280, 80))
        self.frame.setMinimumSize(QtCore.QSize(0, 80))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 120))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_1 = QtWidgets.QLabel(self.frame)
        self.label_1.setGeometry(QtCore.QRect(20, 10, 120, 60))
        self.label_1.setStyleSheet("font: 14pt \"微软雅黑\";")
        self.label_1.setAlignment(QtCore.Qt.AlignCenter)
        self.label_1.setObjectName("label_1")
        self.min_version = QtWidgets.QLineEdit(self.frame)
        self.min_version.setGeometry(QtCore.QRect(140, 10, 120, 60))
        self.min_version.setStyleSheet("font: 18pt \"微软雅黑\";\n"
"color: rgb(0, 0, 255);")
        self.min_version.setAlignment(QtCore.Qt.AlignCenter)
        self.min_version.setObjectName("min_version")
        self.label_2 = QtWidgets.QLabel(self.frame)
        self.label_2.setGeometry(QtCore.QRect(280, 10, 120, 60))
        self.label_2.setStyleSheet("font: 14pt \"微软雅黑\";")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.max_version = QtWidgets.QLineEdit(self.frame)
        self.max_version.setGeometry(QtCore.QRect(400, 10, 120, 60))
        self.max_version.setStyleSheet("font: 18pt \"微软雅黑\";\n"
"color: rgb(0, 0, 255);")
        self.max_version.setAlignment(QtCore.Qt.AlignCenter)
        self.max_version.setObjectName("max_version")
        self.label_3 = QtWidgets.QLabel(self.frame)
        self.label_3.setGeometry(QtCore.QRect(540, 10, 120, 60))
        self.label_3.setStyleSheet("font: 14pt \"微软雅黑\";")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.priority = QtWidgets.QLineEdit(self.frame)
        self.priority.setGeometry(QtCore.QRect(660, 10, 120, 60))
        self.priority.setStyleSheet("font: 18pt \"微软雅黑\";\n"
"color: rgb(0, 0, 255);")
        self.priority.setAlignment(QtCore.Qt.AlignCenter)
        self.priority.setObjectName("priority")
        self.label_4 = QtWidgets.QLabel(self.frame)
        self.label_4.setGeometry(QtCore.QRect(800, 10, 360, 20))
        self.label_4.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_4.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(self.frame)
        self.label_5.setGeometry(QtCore.QRect(800, 30, 360, 20))
        self.label_5.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_5.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(self.frame)
        self.label_6.setGeometry(QtCore.QRect(800, 50, 360, 20))
        self.label_6.setStyleSheet("font: 12pt \"微软雅黑\";")
        self.label_6.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignVCenter)
        self.label_6.setObjectName("label_6")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_1.setText(_translate("Form", "最小版本号"))
        self.label_2.setText(_translate("Form", "最大版本号"))
        self.label_3.setText(_translate("Form", "优先级"))
        self.label_4.setText(_translate("Form", "1 : 每隔3天弹出一次更新提示"))
        self.label_5.setText(_translate("Form", "2 : 每隔1天弹出一次更新提示"))
        self.label_6.setText(_translate("Form", "3 : 每次进入弹出（强制全屏提示）"))