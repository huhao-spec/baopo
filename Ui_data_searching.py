# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'd:\360MoveData\Users\12433\Desktop\Solution_crystallization\project\data_searching.ui'
#
# Created by: PyQt5 UI code generator 5.15.9
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(1266, 867)
        self.verticalLayoutWidget = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget.setGeometry(QtCore.QRect(140, 130, 351, 151))
        self.verticalLayoutWidget.setObjectName("verticalLayoutWidget")
        self.main_Layout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget)
        self.main_Layout.setContentsMargins(0, 0, 0, 0)
        self.main_Layout.setObjectName("main_Layout")
        self.data_source_Layout = QtWidgets.QHBoxLayout()
        self.data_source_Layout.setObjectName("data_source_Layout")
        self.data_source_labal = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.data_source_labal.setObjectName("data_source_labal")
        self.data_source_Layout.addWidget(self.data_source_labal)
        self.data_source = QtWidgets.QComboBox(self.verticalLayoutWidget)
        self.data_source.setObjectName("data_source")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.data_source.addItem("")
        self.data_source_Layout.addWidget(self.data_source)
        self.main_Layout.addLayout(self.data_source_Layout)
        self.time_Layout = QtWidgets.QHBoxLayout()
        self.time_Layout.setObjectName("time_Layout")
        self.time_from_labal = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.time_from_labal.setObjectName("time_from_labal")
        self.time_Layout.addWidget(self.time_from_labal)
        self.s_datetime = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.s_datetime.setObjectName("s_datetime")
        self.time_Layout.addWidget(self.s_datetime)
        self.to_labal = QtWidgets.QLabel(self.verticalLayoutWidget)
        self.to_labal.setObjectName("to_labal")
        self.time_Layout.addWidget(self.to_labal)
        self.e_datetime = QtWidgets.QDateTimeEdit(self.verticalLayoutWidget)
        self.e_datetime.setObjectName("e_datetime")
        self.time_Layout.addWidget(self.e_datetime)
        self.main_Layout.addLayout(self.time_Layout)
        self.sql_table_show = QtWidgets.QTableWidget(Form)
        self.sql_table_show.setGeometry(QtCore.QRect(110, 290, 631, 321))
        self.sql_table_show.setObjectName("sql_table_show")
        self.sql_table_show.setColumnCount(0)
        self.sql_table_show.setRowCount(0)
        self.verticalLayoutWidget_2 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_2.setGeometry(QtCore.QRect(500, 160, 221, 101))
        self.verticalLayoutWidget_2.setObjectName("verticalLayoutWidget_2")
        self.verticalLayout = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.tem_limited_Layout = QtWidgets.QHBoxLayout()
        self.tem_limited_Layout.setObjectName("tem_limited_Layout")
        self.tem_limit_show = QtWidgets.QLabel(self.verticalLayoutWidget_2)
        self.tem_limit_show.setObjectName("tem_limit_show")
        self.tem_limited_Layout.addWidget(self.tem_limit_show)
        self.tem_limit = QtWidgets.QDoubleSpinBox(self.verticalLayoutWidget_2)
        self.tem_limit.setObjectName("tem_limit")
        self.tem_limited_Layout.addWidget(self.tem_limit)
        self.verticalLayout.addLayout(self.tem_limited_Layout)
        self.tem_limit_update = QtWidgets.QPushButton(self.verticalLayoutWidget_2)
        self.tem_limit_update.setObjectName("tem_limit_update")
        self.verticalLayout.addWidget(self.tem_limit_update)
        self.verticalLayoutWidget_3 = QtWidgets.QWidget(Form)
        self.verticalLayoutWidget_3.setGeometry(QtCore.QRect(360, 620, 169, 80))
        self.verticalLayoutWidget_3.setObjectName("verticalLayoutWidget_3")
        self.verticalLayout_3 = QtWidgets.QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_3.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.tem_limit_on_off = QtWidgets.QCheckBox(self.verticalLayoutWidget_3)
        self.tem_limit_on_off.setObjectName("tem_limit_on_off")
        self.verticalLayout_3.addWidget(self.tem_limit_on_off)
        self.Confirm_button = QtWidgets.QPushButton(self.verticalLayoutWidget_3)
        self.Confirm_button.setObjectName("Confirm_button")
        self.verticalLayout_3.addWidget(self.Confirm_button)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.data_source_labal.setText(_translate("Form", "<html><head/><body><p align=\"center\">数据源:</p></body></html>"))
        self.data_source.setItemText(0, _translate("Form", "01罐"))
        self.data_source.setItemText(1, _translate("Form", "02罐"))
        self.data_source.setItemText(2, _translate("Form", "03罐"))
        self.data_source.setItemText(3, _translate("Form", "全部"))
        self.time_from_labal.setText(_translate("Form", "时间从:"))
        self.to_labal.setText(_translate("Form", "到:"))
        self.tem_limit_show.setText(_translate("Form", "临界温度设置:"))
        self.tem_limit_update.setText(_translate("Form", "临界温度设置"))
        self.tem_limit_on_off.setText(_translate("Form", "单独查询临界温度以上数据"))
        self.Confirm_button.setText(_translate("Form", "提交"))
