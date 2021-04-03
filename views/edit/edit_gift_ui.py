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
        Form.resize(1800, 900)
        Form.setStyleSheet("background-color: rgb(247, 247, 247);")
        self.horizontalLayout = QtWidgets.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setObjectName("verticalLayout")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setMinimumSize(QtCore.QSize(120, 40))
        self.label_10.setMaximumSize(QtCore.QSize(120, 40))
        self.label_10.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_10.setAlignment(QtCore.Qt.AlignCenter)
        self.label_10.setObjectName("label_10")
        self.horizontalLayout_3.addWidget(self.label_10)
        self.file_name = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.file_name.sizePolicy().hasHeightForWidth())
        self.file_name.setSizePolicy(sizePolicy)
        self.file_name.setMinimumSize(QtCore.QSize(0, 40))
        self.file_name.setMaximumSize(QtCore.QSize(16777215, 40))
        self.file_name.setStyleSheet("font: 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.file_name.setText("")
        self.file_name.setAlignment(QtCore.Qt.AlignCenter)
        self.file_name.setObjectName("file_name")
        self.horizontalLayout_3.addWidget(self.file_name)
        self.pushButton = QtWidgets.QPushButton(Form)
        self.pushButton.setMinimumSize(QtCore.QSize(100, 40))
        self.pushButton.setMaximumSize(QtCore.QSize(100, 40))
        self.pushButton.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 255);")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_3.addWidget(self.pushButton)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label_12 = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_12.sizePolicy().hasHeightForWidth())
        self.label_12.setSizePolicy(sizePolicy)
        self.label_12.setMinimumSize(QtCore.QSize(120, 40))
        self.label_12.setMaximumSize(QtCore.QSize(120, 40))
        self.label_12.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_12.setAlignment(QtCore.Qt.AlignCenter)
        self.label_12.setObjectName("label_12")
        self.horizontalLayout_4.addWidget(self.label_12)
        self.language = QtWidgets.QLabel(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.language.sizePolicy().hasHeightForWidth())
        self.language.setSizePolicy(sizePolicy)
        self.language.setMinimumSize(QtCore.QSize(0, 40))
        self.language.setMaximumSize(QtCore.QSize(16777215, 40))
        self.language.setStyleSheet("font: 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);\n"
"background-color: rgb(255, 255, 255);")
        self.language.setText("")
        self.language.setAlignment(QtCore.Qt.AlignCenter)
        self.language.setObjectName("language")
        self.horizontalLayout_4.addWidget(self.language)
        self.pushButton_2 = QtWidgets.QPushButton(Form)
        self.pushButton_2.setMinimumSize(QtCore.QSize(100, 40))
        self.pushButton_2.setMaximumSize(QtCore.QSize(100, 40))
        self.pushButton_2.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(255, 255, 255);\n"
"background-color: rgb(85, 85, 255);")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_4.addWidget(self.pushButton_2)
        self.verticalLayout.addLayout(self.horizontalLayout_4)
        self.tableWidget = QtWidgets.QTableWidget(Form)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(0)
        self.tableWidget.setRowCount(0)
        self.verticalLayout.addWidget(self.tableWidget)
        self.horizontalLayout.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtWidgets.QVBoxLayout()
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.frame_2 = QtWidgets.QFrame(Form)
        self.frame_2.setMinimumSize(QtCore.QSize(560, 160))
        self.frame_2.setMaximumSize(QtCore.QSize(560, 160))
        self.frame_2.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.ijoysoft_icon = QtWidgets.QLabel(self.frame_2)
        self.ijoysoft_icon.setGeometry(QtCore.QRect(167, 20, 226, 120))
        self.ijoysoft_icon.setText("")
        self.ijoysoft_icon.setObjectName("ijoysoft_icon")
        self.verticalLayout_2.addWidget(self.frame_2)
        self.frame_3 = QtWidgets.QFrame(Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Preferred, QtWidgets.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(33)
        sizePolicy.setHeightForWidth(self.frame_3.sizePolicy().hasHeightForWidth())
        self.frame_3.setSizePolicy(sizePolicy)
        self.frame_3.setMinimumSize(QtCore.QSize(560, 390))
        self.frame_3.setMaximumSize(QtCore.QSize(560, 390))
        self.frame_3.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame_3.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_3.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_3.setObjectName("frame_3")
        self.dialog_limit = QtWidgets.QLineEdit(self.frame_3)
        self.dialog_limit.setGeometry(QtCore.QRect(430, 230, 120, 30))
        self.dialog_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_limit.setObjectName("dialog_limit")
        self.label_6 = QtWidgets.QLabel(self.frame_3)
        self.label_6.setGeometry(QtCore.QRect(380, 190, 40, 30))
        self.label_6.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_6.setObjectName("label_6")
        self.list_limit = QtWidgets.QLineEdit(self.frame_3)
        self.list_limit.setGeometry(QtCore.QRect(430, 190, 120, 30))
        self.list_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.list_limit.setObjectName("list_limit")
        self.label_5 = QtWidgets.QLabel(self.frame_3)
        self.label_5.setGeometry(QtCore.QRect(380, 150, 40, 30))
        self.label_5.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_5.setObjectName("label_5")
        self.dialog_title = QtWidgets.QLabel(self.frame_3)
        self.dialog_title.setGeometry(QtCore.QRect(10, 230, 100, 30))
        self.dialog_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.dialog_title.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_title.setObjectName("dialog_title")
        self.dialog_index = QtWidgets.QLineEdit(self.frame_3)
        self.dialog_index.setGeometry(QtCore.QRect(120, 230, 120, 30))
        self.dialog_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_index.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_index.setObjectName("dialog_index")
        self.interstitial_index = QtWidgets.QLineEdit(self.frame_3)
        self.interstitial_index.setGeometry(QtCore.QRect(120, 150, 120, 30))
        self.interstitial_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_index.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_index.setObjectName("interstitial_index")
        self.sidebar_count = QtWidgets.QLineEdit(self.frame_3)
        self.sidebar_count.setGeometry(QtCore.QRect(250, 310, 120, 30))
        self.sidebar_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_count.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_count.setObjectName("sidebar_count")
        self.label_3 = QtWidgets.QLabel(self.frame_3)
        self.label_3.setGeometry(QtCore.QRect(430, 70, 120, 30))
        self.label_3.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.label = QtWidgets.QLabel(self.frame_3)
        self.label.setGeometry(QtCore.QRect(120, 70, 120, 30))
        self.label.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.label_7 = QtWidgets.QLabel(self.frame_3)
        self.label_7.setGeometry(QtCore.QRect(380, 230, 40, 30))
        self.label_7.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_7.setObjectName("label_7")
        self.sidebar_limit = QtWidgets.QLineEdit(self.frame_3)
        self.sidebar_limit.setGeometry(QtCore.QRect(430, 310, 120, 30))
        self.sidebar_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_limit.setObjectName("sidebar_limit")
        self.carousel_title = QtWidgets.QLabel(self.frame_3)
        self.carousel_title.setGeometry(QtCore.QRect(10, 270, 100, 30))
        self.carousel_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.carousel_title.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_title.setObjectName("carousel_title")
        self.label_2 = QtWidgets.QLabel(self.frame_3)
        self.label_2.setGeometry(QtCore.QRect(250, 70, 120, 30))
        self.label_2.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.label_8 = QtWidgets.QLabel(self.frame_3)
        self.label_8.setGeometry(QtCore.QRect(380, 270, 40, 30))
        self.label_8.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_8.setObjectName("label_8")
        self.interstitial_count = QtWidgets.QLineEdit(self.frame_3)
        self.interstitial_count.setGeometry(QtCore.QRect(250, 150, 120, 30))
        self.interstitial_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_count.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_count.setObjectName("interstitial_count")
        self.rate_count = QtWidgets.QLineEdit(self.frame_3)
        self.rate_count.setGeometry(QtCore.QRect(250, 110, 120, 30))
        self.rate_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_count.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_count.setObjectName("rate_count")
        self.list_count = QtWidgets.QLineEdit(self.frame_3)
        self.list_count.setGeometry(QtCore.QRect(250, 190, 120, 30))
        self.list_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_count.setAlignment(QtCore.Qt.AlignCenter)
        self.list_count.setObjectName("list_count")
        self.sidebar_title = QtWidgets.QLabel(self.frame_3)
        self.sidebar_title.setGeometry(QtCore.QRect(10, 310, 100, 30))
        self.sidebar_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.sidebar_title.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_title.setObjectName("sidebar_title")
        self.carousel_count = QtWidgets.QLineEdit(self.frame_3)
        self.carousel_count.setGeometry(QtCore.QRect(250, 270, 120, 30))
        self.carousel_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_count.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_count.setObjectName("carousel_count")
        self.rate_index = QtWidgets.QLineEdit(self.frame_3)
        self.rate_index.setGeometry(QtCore.QRect(120, 110, 120, 30))
        self.rate_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_index.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_index.setObjectName("rate_index")
        self.list_title = QtWidgets.QLabel(self.frame_3)
        self.list_title.setGeometry(QtCore.QRect(10, 190, 100, 30))
        self.list_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.list_title.setAlignment(QtCore.Qt.AlignCenter)
        self.list_title.setObjectName("list_title")
        self.wall_index = QtWidgets.QLineEdit(self.frame_3)
        self.wall_index.setGeometry(QtCore.QRect(120, 350, 120, 30))
        self.wall_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.wall_index.setAlignment(QtCore.Qt.AlignCenter)
        self.wall_index.setObjectName("wall_index")
        self.dialog_count = QtWidgets.QLineEdit(self.frame_3)
        self.dialog_count.setGeometry(QtCore.QRect(250, 230, 120, 30))
        self.dialog_count.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.dialog_count.setAlignment(QtCore.Qt.AlignCenter)
        self.dialog_count.setObjectName("dialog_count")
        self.label_9 = QtWidgets.QLabel(self.frame_3)
        self.label_9.setGeometry(QtCore.QRect(380, 310, 40, 30))
        self.label_9.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_9.setObjectName("label_9")
        self.rate_limit = QtWidgets.QLineEdit(self.frame_3)
        self.rate_limit.setGeometry(QtCore.QRect(430, 110, 120, 30))
        self.rate_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.rate_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_limit.setObjectName("rate_limit")
        self.list_index = QtWidgets.QLineEdit(self.frame_3)
        self.list_index.setGeometry(QtCore.QRect(120, 190, 120, 30))
        self.list_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.list_index.setAlignment(QtCore.Qt.AlignCenter)
        self.list_index.setObjectName("list_index")
        self.wall_title = QtWidgets.QLabel(self.frame_3)
        self.wall_title.setGeometry(QtCore.QRect(10, 350, 100, 30))
        self.wall_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.wall_title.setAlignment(QtCore.Qt.AlignCenter)
        self.wall_title.setObjectName("wall_title")
        self.label_4 = QtWidgets.QLabel(self.frame_3)
        self.label_4.setGeometry(QtCore.QRect(380, 110, 40, 30))
        self.label_4.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.label_4.setObjectName("label_4")
        self.rate_title = QtWidgets.QLabel(self.frame_3)
        self.rate_title.setGeometry(QtCore.QRect(10, 110, 100, 30))
        self.rate_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.rate_title.setAlignment(QtCore.Qt.AlignCenter)
        self.rate_title.setObjectName("rate_title")
        self.carousel_index = QtWidgets.QLineEdit(self.frame_3)
        self.carousel_index.setGeometry(QtCore.QRect(120, 270, 120, 30))
        self.carousel_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_index.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_index.setObjectName("carousel_index")
        self.interstitial_title = QtWidgets.QLabel(self.frame_3)
        self.interstitial_title.setGeometry(QtCore.QRect(10, 150, 100, 30))
        self.interstitial_title.setStyleSheet("font: 12pt \"微软雅黑\";\n"
"background-color: rgb(255, 255, 255);")
        self.interstitial_title.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_title.setObjectName("interstitial_title")
        self.sidebar_index = QtWidgets.QLineEdit(self.frame_3)
        self.sidebar_index.setGeometry(QtCore.QRect(120, 310, 120, 30))
        self.sidebar_index.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.sidebar_index.setAlignment(QtCore.Qt.AlignCenter)
        self.sidebar_index.setObjectName("sidebar_index")
        self.carousel_limit = QtWidgets.QLineEdit(self.frame_3)
        self.carousel_limit.setGeometry(QtCore.QRect(430, 270, 120, 30))
        self.carousel_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.carousel_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.carousel_limit.setObjectName("carousel_limit")
        self.interstitial_limit = QtWidgets.QLineEdit(self.frame_3)
        self.interstitial_limit.setGeometry(QtCore.QRect(430, 150, 120, 30))
        self.interstitial_limit.setStyleSheet("background-color: rgb(255, 255, 255);\n"
"font: 75 14pt \"微软雅黑\";\n"
"color: rgb(85, 85, 255);")
        self.interstitial_limit.setAlignment(QtCore.Qt.AlignCenter)
        self.interstitial_limit.setObjectName("interstitial_limit")
        self.label_13 = QtWidgets.QLabel(self.frame_3)
        self.label_13.setGeometry(QtCore.QRect(10, 10, 540, 40))
        self.label_13.setStyleSheet("font: 20pt \"微软雅黑\";")
        self.label_13.setAlignment(QtCore.Qt.AlignCenter)
        self.label_13.setObjectName("label_13")
        self.verticalLayout_2.addWidget(self.frame_3)
        self.frame_4 = QtWidgets.QFrame(Form)
        self.frame_4.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_4.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_4.setObjectName("frame_4")
        self.verticalLayout_2.addWidget(self.frame_4)
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setMinimumSize(QtCore.QSize(0, 140))
        self.frame.setMaximumSize(QtCore.QSize(16777215, 140))
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.refresh_ui = QtWidgets.QPushButton(self.frame)
        self.refresh_ui.setGeometry(QtCore.QRect(200, 20, 160, 40))
        self.refresh_ui.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.refresh_ui.setObjectName("refresh_ui")
        self.add_gift_wall = QtWidgets.QPushButton(self.frame)
        self.add_gift_wall.setGeometry(QtCore.QRect(380, 20, 160, 40))
        self.add_gift_wall.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.add_gift_wall.setObjectName("add_gift_wall")
        self.reload_data = QtWidgets.QPushButton(self.frame)
        self.reload_data.setGeometry(QtCore.QRect(20, 20, 160, 40))
        self.reload_data.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.reload_data.setObjectName("reload_data")
        self.create_gift_wall_file = QtWidgets.QPushButton(self.frame)
        self.create_gift_wall_file.setGeometry(QtCore.QRect(20, 80, 160, 40))
        self.create_gift_wall_file.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.create_gift_wall_file.setObjectName("create_gift_wall_file")
        self.open_outputs = QtWidgets.QPushButton(self.frame)
        self.open_outputs.setGeometry(QtCore.QRect(200, 80, 160, 40))
        self.open_outputs.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.open_outputs.setObjectName("open_outputs")
        self.clear_outputs = QtWidgets.QPushButton(self.frame)
        self.clear_outputs.setGeometry(QtCore.QRect(380, 80, 160, 40))
        self.clear_outputs.setStyleSheet("background-color: rgb(85, 85, 255);\n"
"color: rgb(255, 255, 255);\n"
"font: 12pt \"微软雅黑\";")
        self.clear_outputs.setObjectName("clear_outputs")
        self.verticalLayout_2.addWidget(self.frame)
        self.horizontalLayout.addLayout(self.verticalLayout_2)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label_10.setText(_translate("Form", "选择输出文件名"))
        self.pushButton.setText(_translate("Form", "选择"))
        self.label_12.setText(_translate("Form", "选择输出地区"))
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
        self.label_13.setText(_translate("Form", "GiftWall配置"))
        self.refresh_ui.setText(_translate("Form", "刷新界面"))
        self.add_gift_wall.setText(_translate("Form", "添加GiftWall"))
        self.reload_data.setText(_translate("Form", "更新配置和图标"))
        self.create_gift_wall_file.setText(_translate("Form", "生成GiftWall配置表"))
        self.open_outputs.setText(_translate("Form", "查看Outputs"))
        self.clear_outputs.setText(_translate("Form", "清空Outputs"))
