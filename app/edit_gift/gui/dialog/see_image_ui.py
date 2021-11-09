# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'see_image_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not main this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1000, 820)
        Form.setMinimumSize(QtCore.QSize(1000, 820))
        Form.setMaximumSize(QtCore.QSize(1000, 820))
        self.formLayout = QtWidgets.QFormLayout(Form)
        self.formLayout.setObjectName("formLayout")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.icon = QtWidgets.QLabel(Form)
        self.icon.setMinimumSize(QtCore.QSize(180, 800))
        self.icon.setMaximumSize(QtCore.QSize(180, 800))
        self.icon.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.icon.setText("")
        self.icon.setAlignment(QtCore.Qt.AlignCenter)
        self.icon.setObjectName("icon")
        self.horizontalLayout.addWidget(self.icon)
        self.poster = QtWidgets.QLabel(Form)
        self.poster.setMinimumSize(QtCore.QSize(180, 800))
        self.poster.setMaximumSize(QtCore.QSize(1000, 800))
        self.poster.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.poster.setText("")
        self.poster.setAlignment(QtCore.Qt.AlignCenter)
        self.poster.setObjectName("poster")
        self.horizontalLayout.addWidget(self.poster)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
