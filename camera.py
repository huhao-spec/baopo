# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'camera.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow3(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1150, 800)
        font = QtGui.QFont()
        font.setPointSize(9)
        MainWindow.setFont(font)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/中国兵器工业集团logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.horizontalLayout_10 = QtWidgets.QHBoxLayout(self.frame)
        self.horizontalLayout_10.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_10.setSpacing(0)
        self.horizontalLayout_10.setObjectName("horizontalLayout_10")
        self.verticalLayout_camera = QtWidgets.QVBoxLayout()
        self.verticalLayout_camera.setSpacing(0)
        self.verticalLayout_camera.setObjectName("verticalLayout_camera")
        self.label_cameratime = QtWidgets.QLabel(self.frame)
        self.label_cameratime.setStyleSheet("background-color: rgb(245,245,220);\n"
"")
        self.label_cameratime.setText("")
        self.label_cameratime.setObjectName("label_cameratime")
        self.verticalLayout_camera.addWidget(self.label_cameratime)
        self.horizontalLayout_10.addLayout(self.verticalLayout_camera)
        self.frame_5 = QtWidgets.QFrame(self.frame)
        self.frame_5.setAutoFillBackground(False)
        self.frame_5.setStyleSheet("background-color: rgb(245,245,220);\n"
"\n"
"")
        self.frame_5.setFrameShape(QtWidgets.QFrame.Box)
        self.frame_5.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.frame_5.setLineWidth(2)
        self.frame_5.setMidLineWidth(2)
        self.frame_5.setObjectName("frame_5")
        self.verticalLayout_8 = QtWidgets.QVBoxLayout(self.frame_5)
        self.verticalLayout_8.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_8.setSpacing(0)
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_14 = QtWidgets.QLabel(self.frame_5)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(25)
        self.label_14.setFont(font)
        self.label_14.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.label_14.setAlignment(QtCore.Qt.AlignCenter)
        self.label_14.setObjectName("label_14")
        self.verticalLayout_8.addWidget(self.label_14)
        self.widget_8 = QtWidgets.QWidget(self.frame_5)
        self.widget_8.setAutoFillBackground(False)
        self.widget_8.setObjectName("widget_8")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.widget_8)
        self.gridLayout_3.setContentsMargins(9, 9, 9, 9)
        self.gridLayout_3.setHorizontalSpacing(0)
        self.gridLayout_3.setVerticalSpacing(20)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.label_tem = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_tem.setFont(font)
        self.label_tem.setAlignment(QtCore.Qt.AlignCenter)
        self.label_tem.setObjectName("label_tem")
        self.gridLayout_3.addWidget(self.label_tem, 5, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.lineEdit_jj = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_jj.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_jj.setFont(font)
        self.lineEdit_jj.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_jj.setReadOnly(True)
        self.lineEdit_jj.setObjectName("lineEdit_jj")
        self.gridLayout_3.addWidget(self.lineEdit_jj, 3, 1, 1, 1)
        self.label = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label.setFont(font)
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.gridLayout_3.addWidget(self.label, 8, 0, 1, 1)
        self.label_midu = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_midu.setFont(font)
        self.label_midu.setAlignment(QtCore.Qt.AlignCenter)
        self.label_midu.setObjectName("label_midu")
        self.gridLayout_3.addWidget(self.label_midu, 6, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_time = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_time.setFont(font)
        self.label_time.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.label_time.setObjectName("label_time")
        self.gridLayout_3.addWidget(self.label_time, 9, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.label_camera = QtWidgets.QLabel(self.widget_8)
        self.label_camera.setMinimumSize(QtCore.QSize(0, 0))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_camera.setFont(font)
        self.label_camera.setAlignment(QtCore.Qt.AlignCenter)
        self.label_camera.setObjectName("label_camera")
        self.gridLayout_3.addWidget(self.label_camera, 1, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.lineEdit_camera = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_camera.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_camera.setFont(font)
        self.lineEdit_camera.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_camera.setReadOnly(True)
        self.lineEdit_camera.setObjectName("lineEdit_camera")
        self.gridLayout_3.addWidget(self.lineEdit_camera, 1, 1, 1, 1)
        self.label_zhuangtai = QtWidgets.QLabel(self.widget_8)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_zhuangtai.setFont(font)
        self.label_zhuangtai.setAlignment(QtCore.Qt.AlignCenter)
        self.label_zhuangtai.setObjectName("label_zhuangtai")
        self.gridLayout_3.addWidget(self.label_zhuangtai, 3, 0, 1, 1, QtCore.Qt.AlignHCenter)
        self.lineEdit_tem = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_tem.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_tem.setFont(font)
        self.lineEdit_tem.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_tem.setReadOnly(True)
        self.lineEdit_tem.setObjectName("lineEdit_tem")
        self.gridLayout_3.addWidget(self.lineEdit_tem, 5, 1, 1, 1)
        self.lineEdit_density = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_density.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_density.setFont(font)
        self.lineEdit_density.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_density.setReadOnly(True)
        self.lineEdit_density.setObjectName("lineEdit_density")
        self.gridLayout_3.addWidget(self.lineEdit_density, 6, 1, 1, 1)
        self.lineEdit_ph = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_ph.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_ph.setFont(font)
        self.lineEdit_ph.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_ph.setReadOnly(True)
        self.lineEdit_ph.setObjectName("lineEdit_ph")
        self.gridLayout_3.addWidget(self.lineEdit_ph, 8, 1, 1, 1)
        self.lineEdit_time = QtWidgets.QLineEdit(self.widget_8)
        self.lineEdit_time.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setPointSize(15)
        self.lineEdit_time.setFont(font)
        self.lineEdit_time.setStyleSheet("border-radius:10px;\n"
"border:1px solid rgb(100,100,189)")
        self.lineEdit_time.setReadOnly(True)
        self.lineEdit_time.setObjectName("lineEdit_time")
        self.gridLayout_3.addWidget(self.lineEdit_time, 9, 1, 1, 1)
        self.verticalLayout_8.addWidget(self.widget_8)
        self.gridLayout_2 = QtWidgets.QGridLayout()
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.pushButton_start = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_start.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_start.setFont(font)
        self.pushButton_start.setStyleSheet("QPushButton#pushButton_start{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"border:2px solid rgb(255,255,255);\n"
"}\n"
"QPushButton#pushButton_start:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_start:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_start.setObjectName("pushButton_start")
        self.gridLayout_2.addWidget(self.pushButton_start, 0, 0, 1, 1)
        self.pushButton_end = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_end.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_end.setFont(font)
        self.pushButton_end.setStyleSheet("QPushButton#pushButton_end{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_end:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_end:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_end.setObjectName("pushButton_end")
        self.gridLayout_2.addWidget(self.pushButton_end, 2, 2, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem, 1, 0, 1, 1)
        self.pushButton_light = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_light.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_light.setFont(font)
        self.pushButton_light.setStyleSheet("QPushButton#pushButton_light{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_light:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_light:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_light.setObjectName("pushButton_light")
        self.gridLayout_2.addWidget(self.pushButton_light, 0, 2, 1, 1)
        self.pushButton_wash = QtWidgets.QPushButton(self.frame_5)
        self.pushButton_wash.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_wash.setFont(font)
        self.pushButton_wash.setStyleSheet("QPushButton#pushButton_wash{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_wash:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_wash:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_wash.setObjectName("pushButton_wash")
        self.gridLayout_2.addWidget(self.pushButton_wash, 2, 0, 1, 1)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem1, 0, 1, 1, 1)
        spacerItem2 = QtWidgets.QSpacerItem(20, 10, QtWidgets.QSizePolicy.Minimum, QtWidgets.QSizePolicy.Fixed)
        self.gridLayout_2.addItem(spacerItem2, 3, 0, 1, 1)
        self.verticalLayout_8.addLayout(self.gridLayout_2)
        self.create_report = QtWidgets.QPushButton(self.frame_5)
        self.create_report.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.create_report.setFont(font)
        self.create_report.setStyleSheet("QPushButton#create_report{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#create_report:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#create_report:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.create_report.setObjectName("create_report")
        self.verticalLayout_8.addWidget(self.create_report)
        self.verticalLayout_8.setStretch(1, 7)
        self.verticalLayout_8.setStretch(2, 4)
        self.horizontalLayout_10.addWidget(self.frame_5)
        self.horizontalLayout_10.setStretch(0, 6)
        self.horizontalLayout_10.setStretch(1, 4)
        self.verticalLayout.addWidget(self.frame)
        self.horizontalLayout_6 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_6.setSpacing(0)
        self.horizontalLayout_6.setObjectName("horizontalLayout_6")
        self.verticalLayout_qx = QtWidgets.QVBoxLayout()
        self.verticalLayout_qx.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_qx.setSpacing(0)
        self.verticalLayout_qx.setObjectName("verticalLayout_qx")
        self.horizontalLayout_6.addLayout(self.verticalLayout_qx)
        self.gridFrame = QtWidgets.QFrame(self.centralwidget)
        self.gridFrame.setStyleSheet("background-color: rgb(245,245,220);")
        self.gridFrame.setFrameShape(QtWidgets.QFrame.Box)
        self.gridFrame.setFrameShadow(QtWidgets.QFrame.Sunken)
        self.gridFrame.setLineWidth(2)
        self.gridFrame.setMidLineWidth(2)
        self.gridFrame.setObjectName("gridFrame")
        self.gridLayout = QtWidgets.QGridLayout(self.gridFrame)
        self.gridLayout.setSpacing(0)
        self.gridLayout.setObjectName("gridLayout")
        self.progressBar_cx = QtWidgets.QProgressBar(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic Semilight")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.progressBar_cx.setFont(font)
        self.progressBar_cx.setStyleSheet("border-radius: 5px;                                \n"
"font: 25 14pt \"Malgun Gothic Semilight\";\n"
"text-align: center;")
        self.progressBar_cx.setProperty("value", 0)
        self.progressBar_cx.setObjectName("progressBar_cx")
        self.gridLayout.addWidget(self.progressBar_cx, 3, 1, 1, 1)
        self.progressBar_start = QtWidgets.QProgressBar(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic Semilight")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.progressBar_start.setFont(font)
        self.progressBar_start.setStyleSheet("border-radius: 5px;                                \n"
"font: 25 14pt \"Malgun Gothic Semilight\";\n"
"text-align: center;\n"
"")
        self.progressBar_start.setProperty("value", 0)
        self.progressBar_start.setObjectName("progressBar_start")
        self.gridLayout.addWidget(self.progressBar_start, 2, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 1)
        self.label_4 = QtWidgets.QLabel(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.label_4.setFont(font)
        self.label_4.setObjectName("label_4")
        self.gridLayout.addWidget(self.label_4, 3, 0, 1, 1)
        self.progressBar_yr = QtWidgets.QProgressBar(self.gridFrame)
        font = QtGui.QFont()
        font.setFamily("Malgun Gothic Semilight")
        font.setPointSize(14)
        font.setBold(False)
        font.setItalic(False)
        font.setWeight(3)
        self.progressBar_yr.setFont(font)
        self.progressBar_yr.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.progressBar_yr.setStyleSheet("border-radius: 5px;                                \n"
"font: 25 14pt \"Malgun Gothic Semilight\";\n"
"text-align: center;")
        self.progressBar_yr.setProperty("value", 0)
        self.progressBar_yr.setObjectName("progressBar_yr")
        self.gridLayout.addWidget(self.progressBar_yr, 1, 1, 1, 1)
        self.horizontalLayout_6.addWidget(self.gridFrame)
        self.horizontalLayout_6.setStretch(0, 7)
        self.horizontalLayout_6.setStretch(1, 3)
        self.verticalLayout.addLayout(self.horizontalLayout_6)
        self.verticalLayout.setStretch(0, 7)
        self.verticalLayout.setStretch(1, 3)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "水相溶液析晶点在线检测系统"))
        self.label_14.setText(_translate("MainWindow", "水相溶液析晶点检测"))
        self.label_tem.setText(_translate("MainWindow", "温度："))
        self.label.setText(_translate("MainWindow", "PH:"))
        self.label_midu.setText(_translate("MainWindow", "密度："))
        self.label_time.setText(_translate("MainWindow", "时间："))
        self.label_camera.setText(_translate("MainWindow", "摄像头序号："))
        self.label_zhuangtai.setText(_translate("MainWindow", "结晶状况："))
        self.pushButton_start.setText(_translate("MainWindow", "开始"))
        self.pushButton_end.setText(_translate("MainWindow", "结束"))
        self.pushButton_light.setText(_translate("MainWindow", "灯光"))
        self.pushButton_wash.setText(_translate("MainWindow", "冲洗"))
        self.create_report.setText(_translate("MainWindow", "生成数据报告"))
        self.label_2.setText(_translate("MainWindow", "预热:"))
        self.label_3.setText(_translate("MainWindow", "检测:"))
        self.label_4.setText(_translate("MainWindow", "冲洗:"))
import resource_rc
