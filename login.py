# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'login.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow1(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(901, 538)
        font = QtGui.QFont()
        font.setPointSize(10)
        MainWindow.setFont(font)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout(self.centralwidget)
        self.horizontalLayout_4.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_4.setSpacing(0)
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_3.setSpacing(0)
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setStyleSheet("border-image:url(:/images/images/title.png);\n"
"border-top-left-radius:10px;\n"
"border-bottom-left-radius:10px;")
        self.label.setText("")
        self.label.setObjectName("label")
        self.horizontalLayout_3.addWidget(self.label)
        self.frame_2 = QtWidgets.QFrame(self.frame)
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.label_2 = QtWidgets.QLabel(self.frame_2)
        self.label_2.setGeometry(QtCore.QRect(0, 0, 361, 541))
        self.label_2.setStyleSheet("border-image:url(:/images/images/back1.png);\n"
"border-top-right-radius:10px;\n"
"border-bottom-right-radius:10px;")
        self.label_2.setLineWidth(-10)
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.widget = QtWidgets.QWidget(self.frame_2)
        self.widget.setGeometry(QtCore.QRect(80, 40, 191, 71))
        self.widget.setObjectName("widget")
        self.horizontalLayout = QtWidgets.QHBoxLayout(self.widget)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout.setSpacing(0)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton.setFont(font)
        self.pushButton.setStyleSheet("#pushButton{\n"
"    border:none;\n"
"}\n"
"#pushButton:focus{\n"
"    color:rgb(186, 186, 186);\n"
"}")
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout.addWidget(self.pushButton)
        self.line = QtWidgets.QFrame(self.widget)
        self.line.setFrameShape(QtWidgets.QFrame.VLine)
        self.line.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.line.setObjectName("line")
        self.horizontalLayout.addWidget(self.line)
        self.pushButton_2 = QtWidgets.QPushButton(self.widget)
        font = QtGui.QFont()
        font.setPointSize(16)
        font.setBold(True)
        font.setWeight(75)
        self.pushButton_2.setFont(font)
        self.pushButton_2.setStyleSheet("#pushButton_2{\n"
"    border:none;\n"
"}\n"
"#pushButton_2:focus{\n"
"    color:rgb(186, 186, 186);\n"
"}")
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout.addWidget(self.pushButton_2)
        self.widget_3 = QtWidgets.QWidget(self.frame_2)
        self.widget_3.setGeometry(QtCore.QRect(290, 0, 61, 41))
        self.widget_3.setObjectName("widget_3")
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout(self.widget_3)
        self.horizontalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2.setSpacing(6)
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.pushButton_5 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_5.setStyleSheet("#pushButton_5{\n"
"    border:none;\n"
"}\n"
"QPushButton#pushButton_5:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"}")
        self.pushButton_5.setText("")
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/minus.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_5.setIcon(icon)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)
        self.pushButton_4 = QtWidgets.QPushButton(self.widget_3)
        self.pushButton_4.setStyleSheet("#pushButton_4{\n"
"    border:none;\n"
"}\n"
"QPushButton#pushButton_4:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"}")
        self.pushButton_4.setText("")
        icon1 = QtGui.QIcon()
        icon1.addPixmap(QtGui.QPixmap(":/icons/icons/close.png"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        self.pushButton_4.setIcon(icon1)
        self.pushButton_4.setObjectName("pushButton_4")
        self.horizontalLayout_2.addWidget(self.pushButton_4)
        self.widget_4 = QtWidgets.QWidget(self.frame_2)
        self.widget_4.setGeometry(QtCore.QRect(30, 110, 301, 331))
        self.widget_4.setStyleSheet("")
        self.widget_4.setObjectName("widget_4")
        self.lineEdit_4 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_4.setGeometry(QtCore.QRect(10, 70, 281, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_4.setFont(font)
        self.lineEdit_4.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
"border:1px solid rgba(0,0,0,0);\n"
"border-radius:7px;\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_4.setEchoMode(QtWidgets.QLineEdit.Normal)
        self.lineEdit_4.setObjectName("lineEdit_4")
        self.lineEdit_5 = QtWidgets.QLineEdit(self.widget_4)
        self.lineEdit_5.setGeometry(QtCore.QRect(10, 150, 281, 60))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_5.setFont(font)
        self.lineEdit_5.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
"border:1px solid rgba(0,0,0,0);\n"
"border-radius:7px;\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_5.setObjectName("lineEdit_5")
        self.pushButton_6 = QtWidgets.QPushButton(self.widget_4)
        self.pushButton_6.setGeometry(QtCore.QRect(60, 230, 181, 50))
        self.pushButton_6.setStyleSheet("QPushButton#pushButton_6{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_6:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_6:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_6.setObjectName("pushButton_6")
        self.widget_2 = QtWidgets.QWidget(self.frame_2)
        self.widget_2.setGeometry(QtCore.QRect(20, 140, 321, 301))
        self.widget_2.setObjectName("widget_2")
        self.lineEdit = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit.setGeometry(QtCore.QRect(20, 40, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit.setFont(font)
        self.lineEdit.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
"border:1px solid rgba(0,0,0,0);\n"
"border-radius:7px;\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit.setObjectName("lineEdit")
        self.lineEdit_2 = QtWidgets.QLineEdit(self.widget_2)
        self.lineEdit_2.setGeometry(QtCore.QRect(20, 130, 281, 61))
        font = QtGui.QFont()
        font.setPointSize(9)
        self.lineEdit_2.setFont(font)
        self.lineEdit_2.setStyleSheet("background-color: rgba(0, 0, 0,0);\n"
"border:1px solid rgba(0,0,0,0);\n"
"border-radius:7px;\n"
"border-color: rgb(0, 0, 0);")
        self.lineEdit_2.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.pushButton_3 = QtWidgets.QPushButton(self.widget_2)
        self.pushButton_3.setGeometry(QtCore.QRect(50, 230, 211, 51))
        self.pushButton_3.setStyleSheet("QPushButton#pushButton_3{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_3:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_3:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_3.setObjectName("pushButton_3")
        self.checkBox = QtWidgets.QCheckBox(self.widget_2)
        self.checkBox.setGeometry(QtCore.QRect(20, 200, 71, 21))
        font = QtGui.QFont()
        font.setPointSize(8)
        self.checkBox.setFont(font)
        self.checkBox.setObjectName("checkBox")
        self.horizontalLayout_3.addWidget(self.frame_2)
        self.horizontalLayout_3.setStretch(0, 6)
        self.horizontalLayout_3.setStretch(1, 4)
        self.horizontalLayout_4.addWidget(self.frame)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.pushButton_5.clicked.connect(MainWindow.showMinimized) # type: ignore
        self.pushButton_4.clicked.connect(MainWindow.close) # type: ignore
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.pushButton.setText(_translate("MainWindow", "登录"))
        self.pushButton_2.setText(_translate("MainWindow", "管理员"))
        self.lineEdit_4.setPlaceholderText(_translate("MainWindow", "账号："))
        self.lineEdit_5.setPlaceholderText(_translate("MainWindow", "密码："))
        self.pushButton_6.setText(_translate("MainWindow", "登录"))
        self.lineEdit.setPlaceholderText(_translate("MainWindow", "账号："))
        self.lineEdit_2.setPlaceholderText(_translate("MainWindow", "密码："))
        self.pushButton_3.setText(_translate("MainWindow", "登录"))
        self.checkBox.setText(_translate("MainWindow", "记住"))
import resource_rc
