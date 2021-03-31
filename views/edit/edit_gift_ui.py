# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'edit_gift_ui.ui'
#
# Created by: PyQt5 UI code generator 5.15.2
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1800, 800)
        Form.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(0, 90))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 120))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label_10 = QtWidgets.QLabel(self.frame)
        self.label_10.setGeometry(QtCore.QRect(10, 10, 160, 30))
        self.label_10.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(self.frame)
        self.label_11.setGeometry(QtCore.QRect(180, 10, 900, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_11.sizePolicy().hasHeightForWidth())
        self.label_11.setSizePolicy(sizePolicy)
        self.label_11.setMinimumSize(QtCore.QSize(100, 0))
        self.label_11.setStyleSheet("font: 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.label_11.setText("")
        self.label_11.setAlignment(QtCore.Qt.AlignCenter)
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(self.frame)
        self.label_12.setGeometry(QtCore.QRect(10, 50, 160, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(100, 0))
        self.label_12.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(self.frame)
        self.label_13.setGeometry(QtCore.QRect(180, 50, 900, 30))
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_13.sizePolicy().hasHeightForWidth())
        self.label_13.setSizePolicy(sizePolicy)
        self.label_13.setMinimumSize(QtCore.QSize(100, 0))
        self.label_13.setStyleSheet("font: 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.label_13.setText("")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.pushButton = QtWidgets.QPushButton(self.frame)
        self.pushButton.setGeometry(QtCore.QRect(1090, 10, 96, 30))
        self.pushButton.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 255);")
        self.pushButton.setObjectName("pushButton")
        self.pushButton_2 = QtWidgets.QPushButton(self.frame)
        self.pushButton_2.setGeometry(QtCore.QRect(1090, 50, 96, 30))
        self.pushButton_2.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.verticalLayout.addWidget(self.frame)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_1 = QtWidgets.QFrame(Form)
        self.frame_1.setMinimumSize(QtCore.QSize(0, 90))
        self.frame_1.setMaximumSize(QtCore.QSize(16777215, 80))
        self.frame_1.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_1.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_1.setObjectName("frame_1")
        self.verticalLayout_2.addWidget(self.frame_1)
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(560, 0))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.dialog_limit = QtWidgets.QLineEdit(self.frame_2)
        self.dialog_limit.setGeometry(QtCore.QRect(430, 170, 120, 30))
        self.dialog_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_limit.setObjectName("dialog_limit")
        self.label_6 = QtWidgets.QLabel(self.frame_2)
        self.label_6.setGeometry(QtCore.QRect(380, 130, 40, 30))
        self.label_6.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_6.setObjectName("label_6")
        self.list_limit = QtWidgets.QLineEdit(self.frame_2)
        self.list_limit.setGeometry(QtCore.QRect(430, 130, 120, 30))
        self.list_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.list_limit.setObjectName("list_limit")
        self.label_5 = QtWidgets.QLabel(self.frame_2)
        self.label_5.setGeometry(QtCore.QRect(380, 90, 40, 30))
        self.label_5.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_5.setObjectName("label_5")
        self.dialog_title = QtWidgets.QLabel(self.frame_2)
        self.dialog_title.setGeometry(QtCore.QRect(10, 170, 100, 30))
        self.dialog_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.dialog_title.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_title.setObjectName("dialog_title")
        self.dialog_index = QtWidgets.QLineEdit(self.frame_2)
        self.dialog_index.setGeometry(QtCore.QRect(120, 170, 120, 30))
        self.dialog_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_index.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_index.setObjectName("dialog_index")
        self.interstitial_index = QtWidgets.QLineEdit(self.frame_2)
        self.interstitial_index.setGeometry(QtCore.QRect(120, 90, 120, 30))
        self.interstitial_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_index.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_index.setObjectName("interstitial_index")
        self.sidebar_count = QtWidgets.QLineEdit(self.frame_2)
        self.sidebar_count.setGeometry(QtCore.QRect(250, 250, 120, 30))
        self.sidebar_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_count.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_count.setObjectName("sidebar_count")
        self.label_3 = QtWidgets.QLabel(self.frame_2)
        self.label_3.setGeometry(QtCore.QRect(430, 10, 120, 30))
        self.label_3.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.frame_2)
        self.label.setGeometry(QtCore.QRect(120, 10, 120, 30))
        self.label.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.frame_2)
        self.label_7.setGeometry(QtCore.QRect(380, 170, 40, 30))
        self.label_7.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_7.setObjectName("label_7")
        self.sidebar_limit = QtWidgets.QLineEdit(self.frame_2)
        self.sidebar_limit.setGeometry(QtCore.QRect(430, 250, 120, 30))
        self.sidebar_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_limit.setObjectName("sidebar_limit")
        self.carousel_title = QtWidgets.QLabel(self.frame_2)
        self.carousel_title.setGeometry(QtCore.QRect(10, 210, 100, 30))
        self.carousel_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.carousel_title.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_title.setObjectName("carousel_title")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(250, 10, 120, 30))
        self.label_2.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.frame_2)
        self.label_8.setGeometry(QtCore.QRect(380, 210, 40, 30))
        self.label_8.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_8.setObjectName("label_8")
        self.interstitial_count = QtWidgets.QLineEdit(self.frame_2)
        self.interstitial_count.setGeometry(QtCore.QRect(250, 90, 120, 30))
        self.interstitial_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_count.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_count.setObjectName("interstitial_count")
        self.rate_count = QtWidgets.QLineEdit(self.frame_2)
        self.rate_count.setGeometry(QtCore.QRect(250, 50, 120, 30))
        self.rate_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_count.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_count.setObjectName("rate_count")
        self.list_count = QtWidgets.QLineEdit(self.frame_2)
        self.list_count.setGeometry(QtCore.QRect(250, 130, 120, 30))
        self.list_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_count.setAlignment(QtCore.Qt.AlignCenter)
        self.list_count.setObjectName("list_count")
        self.sidebar_title = QtWidgets.QLabel(self.frame_2)
        self.sidebar_title.setGeometry(QtCore.QRect(10, 250, 100, 30))
        self.sidebar_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.sidebar_title.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_title.setObjectName("sidebar_title")
        self.carousel_count = QtWidgets.QLineEdit(self.frame_2)
        self.carousel_count.setGeometry(QtCore.QRect(250, 210, 120, 30))
        self.carousel_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_count.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_count.setObjectName("carousel_count")
        self.rate_index = QtWidgets.QLineEdit(self.frame_2)
        self.rate_index.setGeometry(QtCore.QRect(120, 50, 120, 30))
        self.rate_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_index.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_index.setObjectName("rate_index")
        self.list_title = QtWidgets.QLabel(self.frame_2)
        self.list_title.setGeometry(QtCore.QRect(10, 130, 100, 30))
        self.list_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.list_title.setAlignment(QtCore.Qt.AlignCenter)
        self.list_title.setObjectName("list_title")
        self.wall_index = QtWidgets.QLineEdit(self.frame_2)
        self.wall_index.setGeometry(QtCore.QRect(120, 290, 120, 30))
        self.wall_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.wall_index.setAlignment(QtCore.Qt.AlignCenter)
        self.wall_index.setObjectName("wall_index")
        self.dialog_count = QtWidgets.QLineEdit(self.frame_2)
        self.dialog_count.setGeometry(QtCore.QRect(250, 170, 120, 30))
        self.dialog_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_count.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_count.setObjectName("dialog_count")
        self.label_9 = QtWidgets.QLabel(self.frame_2)
        self.label_9.setGeometry(QtCore.QRect(380, 250, 40, 30))
        self.label_9.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_9.setObjectName("label_9")
        self.rate_limit = QtWidgets.QLineEdit(self.frame_2)
        self.rate_limit.setGeometry(QtCore.QRect(430, 50, 120, 30))
        self.rate_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_limit.setObjectName("rate_limit")
        self.list_index = QtWidgets.QLineEdit(self.frame_2)
        self.list_index.setGeometry(QtCore.QRect(120, 130, 120, 30))
        self.list_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_index.setAlignment(QtCore.Qt.AlignCenter)
        self.list_index.setObjectName("list_index")
        self.wall_title = QtWidgets.QLabel(self.frame_2)
        self.wall_title.setGeometry(QtCore.QRect(10, 290, 100, 30))
        self.wall_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.wall_title.setAlignment(QtCore.Qt.AlignCenter)
        self.wall_title.setObjectName("wall_title")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(380, 50, 40, 30))
        self.label_4.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_4.setObjectName("label_4")
        self.rate_title = QtWidgets.QLabel(self.frame_2)
        self.rate_title.setGeometry(QtCore.QRect(10, 50, 100, 30))
        self.rate_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.rate_title.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_title.setObjectName("rate_title")
        self.carousel_index = QtWidgets.QLineEdit(self.frame_2)
        self.carousel_index.setGeometry(QtCore.QRect(120, 210, 120, 30))
        self.carousel_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_index.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_index.setObjectName("carousel_index")
        self.interstitial_title = QtWidgets.QLabel(self.frame_2)
        self.interstitial_title.setGeometry(QtCore.QRect(10, 90, 100, 30))
        self.interstitial_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.interstitial_title.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_title.setObjectName("interstitial_title")
        self.sidebar_index = QtWidgets.QLineEdit(self.frame_2)
        self.sidebar_index.setGeometry(QtCore.QRect(120, 250, 120, 30))
        self.sidebar_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_index.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_index.setObjectName("sidebar_index")
        self.carousel_limit = QtWidgets.QLineEdit(self.frame_2)
        self.carousel_limit.setGeometry(QtCore.QRect(430, 210, 120, 30))
        self.carousel_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_limit.setObjectName("carousel_limit")
        self.interstitial_limit = QtWidgets.QLineEdit(self.frame_2)
        self.interstitial_limit.setGeometry(QtCore.QRect(430, 90, 120, 30))
        self.interstitial_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_limit.setObjectName("interstitial_limit")
        self.verticalLayout_2.addWidget(self.frame_2)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_10.setText(_translate("Form", "选择输出文件名"))
        self.label_12.setText(_translate("Form", "选择输出地区"))
        self.pushButton.setText(_translate("Form", "选择"))
        self.pushButton_2.setText(_translate("Form", "选择"))
        self.label_6.setText(_translate("Form", "次"))
        self.label_5.setText(_translate("Form", "次"))
        self.dialog_title.setText(_translate("Form", "dialog"))
        self.label_3.setText(_translate("Form", "只展示前几个"))
        self.label.setText(_translate("Form", "第几个开始"))
        self.label_7.setText(_translate("Form", "次"))
        self.carousel_title.setText(_translate("Form", "carousel"))
        self.label_2.setText(_translate("Form", "展示次数/时间"))
        self.label_8.setText(_translate("Form", "毫秒"))
        self.sidebar_title.setText(_translate("Form", "sidebar"))
        self.list_title.setText(_translate("Form", "list"))
        self.label_9.setText(_translate("Form", "次"))
        self.wall_title.setText(_translate("Form", "wall"))
        self.label_4.setText(_translate("Form", "次"))
        self.rate_title.setText(_translate("Form", "rate"))
        self.interstitial_title.setText(_translate("Form", "interstitial"))
