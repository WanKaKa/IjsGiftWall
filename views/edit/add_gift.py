# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'add_gift.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName("Dialog")
        Dialog.resize(1200, 900)
        Dialog.setMinimumSize(QtCore.QSize(1200, 900))
        Dialog.setMaximumSize(QtCore.QSize(1200, 900))
        self.formLayout = QtWidgets.QFormLayout(Dialog)
        self.formLayout.setObjectName("formLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame_2 = QtWidgets.QFrame(Dialog)
        self.frame_2.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_2.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.language_radio_7 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_7.setGeometry(QtCore.QRect(620, 0, 160, 40))
        self.language_radio_7.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_7.setObjectName("language_radio_7")
        self.language_radio_4 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_4.setGeometry(QtCore.QRect(300, 40, 160, 40))
        self.language_radio_4.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_4.setObjectName("language_radio_4")
        self.language_radio_6 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_6.setGeometry(QtCore.QRect(460, 40, 160, 40))
        self.language_radio_6.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_6.setObjectName("language_radio_6")
        self.language_radio_8 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_8.setGeometry(QtCore.QRect(620, 40, 160, 40))
        self.language_radio_8.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_8.setObjectName("language_radio_8")
        self.language_radio_3 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_3.setGeometry(QtCore.QRect(300, 0, 160, 40))
        self.language_radio_3.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_3.setObjectName("language_radio_3")
        self.language_radio_11 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_11.setGeometry(QtCore.QRect(940, 0, 160, 40))
        self.language_radio_11.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_11.setObjectName("language_radio_11")
        self.language_radio_9 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_9.setGeometry(QtCore.QRect(780, 0, 160, 40))
        self.language_radio_9.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_9.setObjectName("language_radio_9")
        self.language_radio_10 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_10.setGeometry(QtCore.QRect(780, 40, 160, 40))
        self.language_radio_10.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_10.setObjectName("language_radio_10")
        self.language_radio_1 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_1.setGeometry(QtCore.QRect(140, 0, 160, 40))
        self.language_radio_1.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_1.setObjectName("language_radio_1")
        self.language_radio_12 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_12.setGeometry(QtCore.QRect(940, 40, 160, 40))
        self.language_radio_12.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_12.setObjectName("language_radio_12")
        self.language_title_2 = QtWidgets.QLabel(self.frame_2)
        self.language_title_2.setGeometry(QtCore.QRect(0, 20, 120, 40))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language_title_2.sizePolicy().hasHeightForWidth())
        self.language_title_2.setSizePolicy(sizePolicy)
        self.language_title_2.setMinimumSize(QtCore.QSize(120, 40))
        self.language_title_2.setMaximumSize(QtCore.QSize(120, 40))
        self.language_title_2.setStyleSheet("font: 10pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.language_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.language_title_2.setObjectName("language_title_2")
        self.language_radio_2 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_2.setGeometry(QtCore.QRect(140, 40, 160, 40))
        self.language_radio_2.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_2.setObjectName("language_radio_2")
        self.language_radio_5 = QtWidgets.QRadioButton(self.frame_2)
        self.language_radio_5.setGeometry(QtCore.QRect(460, 0, 160, 40))
        self.language_radio_5.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.language_radio_5.setObjectName("language_radio_5")
        self.verticalLayout.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Dialog)
        self.frame_3.setMinimumSize(QtCore.QSize(0, 80))
        self.frame_3.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.file_name_radio_8 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_8.setGeometry(QtCore.QRect(620, 40, 160, 40))
        self.file_name_radio_8.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_8.setObjectName("file_name_radio_8")
        self.file_name_title_2 = QtWidgets.QLabel(self.frame_3)
        self.file_name_title_2.setGeometry(QtCore.QRect(0, 20, 120, 40))
        self.file_name_title_2.setMinimumSize(QtCore.QSize(120, 40))
        self.file_name_title_2.setMaximumSize(QtCore.QSize(120, 40))
        self.file_name_title_2.setStyleSheet("font: 10pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.file_name_title_2.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name_title_2.setObjectName("file_name_title_2")
        self.file_name_radio_5 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_5.setGeometry(QtCore.QRect(460, 0, 160, 40))
        self.file_name_radio_5.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_5.setObjectName("file_name_radio_5")
        self.file_name_radio_1 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_1.setGeometry(QtCore.QRect(140, 0, 160, 40))
        self.file_name_radio_1.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_1.setObjectName("file_name_radio_1")
        self.file_name_radio_6 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_6.setGeometry(QtCore.QRect(460, 40, 160, 40))
        self.file_name_radio_6.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_6.setObjectName("file_name_radio_6")
        self.file_name_radio_2 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_2.setGeometry(QtCore.QRect(140, 40, 160, 40))
        self.file_name_radio_2.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_2.setObjectName("file_name_radio_2")
        self.file_name_radio_11 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_11.setGeometry(QtCore.QRect(940, 0, 160, 40))
        self.file_name_radio_11.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_11.setObjectName("file_name_radio_11")
        self.file_name_radio_7 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_7.setGeometry(QtCore.QRect(620, 0, 160, 40))
        self.file_name_radio_7.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_7.setObjectName("file_name_radio_7")
        self.file_name_radio_9 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_9.setGeometry(QtCore.QRect(780, 0, 160, 40))
        self.file_name_radio_9.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_9.setObjectName("file_name_radio_9")
        self.file_name_radio_4 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_4.setGeometry(QtCore.QRect(300, 40, 160, 40))
        self.file_name_radio_4.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_4.setObjectName("file_name_radio_4")
        self.file_name_radio_3 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_3.setGeometry(QtCore.QRect(300, 0, 160, 40))
        self.file_name_radio_3.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_3.setObjectName("file_name_radio_3")
        self.file_name_radio_12 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_12.setGeometry(QtCore.QRect(940, 40, 160, 40))
        self.file_name_radio_12.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_12.setObjectName("file_name_radio_12")
        self.file_name_radio_10 = QtWidgets.QRadioButton(self.frame_3)
        self.file_name_radio_10.setGeometry(QtCore.QRect(780, 40, 160, 40))
        self.file_name_radio_10.setStyleSheet("font: 10pt \"微软雅黑\";")
        self.file_name_radio_10.setObjectName("file_name_radio_10")
        self.verticalLayout.addWidget(self.frame_3)
        self.tableWidget = QtWidgets.QTableWidget(Dialog)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.frame = QtWidgets.QFrame(Dialog)
        self.frame.setMinimumSize(QtCore.QSize(0, 60))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 60))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.add = QtWidgets.QPushButton(self.frame)
        self.add.setGeometry(QtCore.QRect(1010, 10, 160, 40))
        self.add.setMinimumSize(QtCore.QSize(0, 0))
        self.add.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 255);")
        self.add.setObjectName("add")
        self.verticalLayout.addWidget(self.frame)
        self.formLayout.setLayout(0, QtWidgets.QFormLayout.SpanningRole, self.verticalLayout)

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        _translate = QtCore.QCoreApplication.translate
        Dialog.setWindowTitle(_translate("Dialog", "Dialog"))
        self.language_radio_7.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_4.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_6.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_8.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_3.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_11.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_9.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_10.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_1.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_12.setText(_translate("Dialog", "RadioButton"))
        self.language_title_2.setText(_translate("Dialog", "地区"))
        self.language_radio_2.setText(_translate("Dialog", "RadioButton"))
        self.language_radio_5.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_8.setText(_translate("Dialog", "RadioButton"))
        self.file_name_title_2.setText(_translate("Dialog", "文件名"))
        self.file_name_radio_5.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_1.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_6.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_2.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_11.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_7.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_9.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_4.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_3.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_12.setText(_translate("Dialog", "RadioButton"))
        self.file_name_radio_10.setText(_translate("Dialog", "RadioButton"))
        self.add.setText(_translate("Dialog", "添加"))
