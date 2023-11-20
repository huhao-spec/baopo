# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'data_searching.ui'
#
# Created by: PyQt5 UI code generator 5.15.6
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1258, 819)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap(":/icons/icons/中国兵器工业集团logo.svg"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        MainWindow.setStyleSheet("background-color: rgb(222, 222, 222);")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QtWidgets.QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_2.setSpacing(6)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.horizontalLayout_4 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_4.setObjectName("horizontalLayout_4")
        self.label = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(25)
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setStyleSheet("")
        self.label.setAlignment(QtCore.Qt.AlignCenter)
        self.label.setObjectName("label")
        self.horizontalLayout_4.addWidget(self.label)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.data_source_labal = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.data_source_labal.setFont(font)
        self.data_source_labal.setAlignment(QtCore.Qt.AlignCenter)
        self.data_source_labal.setObjectName("data_source_labal")
        self.horizontalLayout.addWidget(self.data_source_labal)
        self.data_source = QtWidgets.QComboBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(12)
        self.data_source.setFont(font)
        self.data_source.setObjectName("data_source")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.horizontalLayout.addWidget(self.data_source)
        spacerItem = QtWidgets.QSpacerItem(250, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem)
        self.tem_limit_show = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.tem_limit_show.setFont(font)
        self.tem_limit_show.setAlignment(QtCore.Qt.AlignCenter)
        self.tem_limit_show.setObjectName("tem_limit_show")
        self.horizontalLayout.addWidget(self.tem_limit_show)
        self.tem_limit = QtWidgets.QDoubleSpinBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(12)
        self.tem_limit.setFont(font)
        self.tem_limit.setMaximum(160.0)
        self.tem_limit.setObjectName("tem_limit")
        self.horizontalLayout.addWidget(self.tem_limit)
        spacerItem1 = QtWidgets.QSpacerItem(40, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem1)
        self.set_pot_lim_tem = QtWidgets.QPushButton(self.centralwidget)
        self.set_pot_lim_tem.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.set_pot_lim_tem.setFont(font)
        self.set_pot_lim_tem.setStyleSheet("QPushButton#set_pot_lim_tem{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#set_pot_lim_tem:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#set_pot_lim_tem:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.set_pot_lim_tem.setObjectName("set_pot_lim_tem")
        self.horizontalLayout.addWidget(self.set_pot_lim_tem)
        spacerItem2 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout.addItem(spacerItem2)
        self.verticalLayout_2.addLayout(self.horizontalLayout)
        self.time_Layout = QtWidgets.QHBoxLayout()
        self.time_Layout.setObjectName("time_Layout")
        self.time_from_labal = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.time_from_labal.setFont(font)
        self.time_from_labal.setAlignment(QtCore.Qt.AlignCenter)
        self.time_from_labal.setObjectName("time_from_labal")
        self.time_Layout.addWidget(self.time_from_labal)
        self.s_datetime = QtWidgets.QDateTimeEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.s_datetime.setFont(font)
        self.s_datetime.setObjectName("s_datetime")
        self.time_Layout.addWidget(self.s_datetime)
        self.to_labal = QtWidgets.QLabel(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.to_labal.setFont(font)
        self.to_labal.setAlignment(QtCore.Qt.AlignCenter)
        self.to_labal.setObjectName("to_labal")
        self.time_Layout.addWidget(self.to_labal)
        self.e_datetime = QtWidgets.QDateTimeEdit(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("Times New Roman")
        font.setPointSize(15)
        self.e_datetime.setFont(font)
        self.e_datetime.setObjectName("e_datetime")
        self.time_Layout.addWidget(self.e_datetime)
        spacerItem3 = QtWidgets.QSpacerItem(150, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.time_Layout.addItem(spacerItem3)
        self.Confirm_button = QtWidgets.QPushButton(self.centralwidget)
        self.Confirm_button.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.Confirm_button.setFont(font)
        self.Confirm_button.setStyleSheet("QPushButton#Confirm_button{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#Confirm_button:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#Confirm_button:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.Confirm_button.setObjectName("Confirm_button")
        self.time_Layout.addWidget(self.Confirm_button)
        spacerItem4 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.time_Layout.addItem(spacerItem4)
        self.print_out = QtWidgets.QPushButton(self.centralwidget)
        self.print_out.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.print_out.setFont(font)
        self.print_out.setStyleSheet("QPushButton#print_out{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#print_out:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#print_out:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.print_out.setObjectName("print_out")
        self.time_Layout.addWidget(self.print_out)
        spacerItem5 = QtWidgets.QSpacerItem(10, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.time_Layout.addItem(spacerItem5)
        self.verticalLayout_2.addLayout(self.time_Layout)
        self.horizontalLayout_3 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        spacerItem6 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem6)
        self.pushButton_tem = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_tem.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_tem.setFont(font)
        self.pushButton_tem.setStyleSheet("QPushButton#pushButton_tem{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_tem:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_tem:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_tem.setObjectName("pushButton_tem")
        self.horizontalLayout_3.addWidget(self.pushButton_tem)
        spacerItem7 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem7)
        self.pushButton_density = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_density.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_density.setFont(font)
        self.pushButton_density.setStyleSheet("QPushButton#pushButton_density{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_density:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_density:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_density.setObjectName("pushButton_density")
        self.horizontalLayout_3.addWidget(self.pushButton_density)
        spacerItem8 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem8)
        self.pushButton_ph = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_ph.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_ph.setFont(font)
        self.pushButton_ph.setStyleSheet("QPushButton#pushButton_ph{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_ph:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_ph:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_ph.setObjectName("pushButton_ph")
        self.horizontalLayout_3.addWidget(self.pushButton_ph)
        spacerItem9 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem9)
        self.pushButton_return = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_return.setMinimumSize(QtCore.QSize(0, 50))
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        font.setPointSize(15)
        self.pushButton_return.setFont(font)
        self.pushButton_return.setStyleSheet("QPushButton#pushButton_return{\n"
"background-color:rgba(2,65,118,255);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_return:hover{\n"
"background-color:rgba(2,65,118,150);\n"
"color:rgba(255,255,255,200);\n"
"border-radius:5px;\n"
"}\n"
"QPushButton#pushButton_return:pressed{\n"
"padding-left:5px;\n"
"padding-top:5px;\n"
"background-color:rgba(2,65,118,100);\n"
"}")
        self.pushButton_return.setObjectName("pushButton_return")
        self.horizontalLayout_3.addWidget(self.pushButton_return)
        spacerItem10 = QtWidgets.QSpacerItem(80, 20, QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem10)
        self.verticalLayout_2.addLayout(self.horizontalLayout_3)
        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.sql_table_show = QtWidgets.QTableWidget(self.centralwidget)
        self.sql_table_show.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.sql_table_show.setObjectName("sql_table_show")
        self.sql_table_show.setColumnCount(0)
        self.sql_table_show.setRowCount(0)
        self.verticalLayout.addWidget(self.sql_table_show)
        self.tem_limit_on_off = QtWidgets.QCheckBox(self.centralwidget)
        font = QtGui.QFont()
        font.setFamily("微软雅黑")
        self.tem_limit_on_off.setFont(font)
        self.tem_limit_on_off.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tem_limit_on_off.setStyleSheet("background-color: rgb(255, 255, 255);")
        self.tem_limit_on_off.setObjectName("tem_limit_on_off")
        self.verticalLayout.addWidget(self.tem_limit_on_off)
        self.verticalLayout.setStretch(1, 1)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        self.verticalLayout_2.setStretch(0, 1)
        self.verticalLayout_2.setStretch(2, 1)
        self.verticalLayout_2.setStretch(3, 1)
        self.verticalLayout_2.setStretch(4, 16)
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "水相溶液析晶点在线检测系统"))
        self.label.setText(_translate("MainWindow", "水相溶液析晶点在线检测系统"))
        self.data_source_labal.setText(_translate("MainWindow", "<html><head/><body><p align=\"center\">数据源:</p></body></html>"))
        self.data_source.setItemText(0, _translate("MainWindow", "01罐"))
        self.data_source.setItemText(1, _translate("MainWindow", "02罐"))
        self.data_source.setItemText(2, _translate("MainWindow", "03罐"))
        self.data_source.setItemText(3, _translate("MainWindow", "全部"))
        self.tem_limit_show.setText(_translate("MainWindow", "临界温度设置:"))
        self.set_pot_lim_tem.setText(_translate("MainWindow", "临界温度设置"))
        self.time_from_labal.setText(_translate("MainWindow", "时间从:"))
        self.to_labal.setText(_translate("MainWindow", "到:"))
        self.Confirm_button.setText(_translate("MainWindow", "查询"))
        self.print_out.setText(_translate("MainWindow", "导出数据"))
        self.pushButton_tem.setText(_translate("MainWindow", "温度记录"))
        self.pushButton_density.setText(_translate("MainWindow", "密度记录"))
        self.pushButton_ph.setText(_translate("MainWindow", "PH值记录"))
        self.pushButton_return.setText(_translate("MainWindow", "返回"))
        self.tem_limit_on_off.setText(_translate("MainWindow", "单独查询临界温度以上数据"))
import resource_rc