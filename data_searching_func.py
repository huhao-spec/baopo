import sys
import time
import pymysql
import pyqtgraph as pg
from data_searching import Ui_MainWindow as Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow 
from PyQt5.QtGui import QPixmap, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy, QHeaderView
from PyQt5.QtCore import QTimer, QDateTime


def database_connect():
        connect = pymysql.connect(
                host = '127.0.0.1' 
                ,user = 'root' 
                ,passwd='123456'
                ,port= 3306
                ,db='test_database'
                ,charset='utf8' 
                )
        return connect

class Ui_search_form(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        self.init_plot()
        self.buttom_set_flag = False
        self.pot = 1
        init_temlmt = self.temlmt_search()[0][0]
        self.ui.tem_limit.setValue(init_temlmt)
        self.ui.Confirm_button.clicked.connect(self.searching)
        self.ui.set_pot_lim_tem.clicked.connect(self.set_pot_lim_tem)

    def init_plot(self): 
        self.ui.s_datetime.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.ui.s_datetime.setCalendarPopup(True)
        self.ui.s_datetime.setDateTime(QDateTime.currentDateTime())

        self.ui.e_datetime.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
        self.ui.e_datetime.setCalendarPopup(True)
        self.ui.e_datetime.setDateTime(QDateTime.currentDateTime())

    def Table_Data(self,i,j,data):

        item = QtWidgets.QTableWidgetItem()
        self.ui.sql_table_show.setItem(i,j, item)
        item = self.ui.sql_table_show.item(i,j)
        tem_limit = float(self.temlmt_search()[0][0]) 
        if j == 1 and float(data) > tem_limit:
            item.setBackground(QColor("yellow"))
        item.setText(self._translate("Form", str(data)))

    def tem_limit_update(self):
        tem_limit = self.ui.tem_limit.value()
        print(tem_limit, self.pot)
        conn = database_connect()
        cur = conn.cursor() 

        sql = "UPDATE tempurter_limit SET tem_limit = %s WHERE pot_num = %s and limit_level = 1;"
        cur.execute(sql, (tem_limit, self.pot))
        conn.commit()

        cur.close()
        conn.close()

    def set_pot_lim_tem(self):
        self.pot = int(self.ui.data_source.currentIndex()) + 1
        self.tem_limit_update()
        self.buttom_set_flag = True

    def temlmt_search(self):
        tem_limited = self.ui.tem_limit.text()
        conn = database_connect()
        cur = conn.cursor()
        try:
            sql = "select tem_limit FROM tempurter_limit where limit_level = 1 and pot_num = %s;"
            cur.execute(sql, (self.pot))
            result = cur.fetchall()
            return result

        except Exception as e:
                # 如果发生错误，打印错误信息
                print(e)

        cur.close()
        conn.close()

    def searching(self):
        if self.buttom_set_flag:
            #dateTime是QDateTimeEdit的一个方法，返回QDateTime时间格式
            #需要再用toPyDateTime转变回python的时间格式
            s_datetime=str(self.ui.s_datetime.dateTime().toPyDateTime())[0:19]
            e_datetime=str(self.ui.e_datetime.dateTime().toPyDateTime())[0:19]
            
            #mysql时间格式转换
            s_datetime_original = time.strptime(s_datetime, "%Y-%m-%d %H:%M:%S")
            s_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S',s_datetime_original)

            e_datetime_original = time.strptime(e_datetime, "%Y-%m-%d %H:%M:%S")
            e_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S',e_datetime_original)


            conn = database_connect()
            cur = conn.cursor()

            sql1 = "SELECT * FROM tempurter WHERE main_time between %s and %s"
            sql2 = "SELECT * FROM tempurter WHERE pot_num = %s and main_time between %s and %s"

            if self.ui.tem_limit_on_off.isChecked():
                tem_limit = float(self.temlmt_search()[0][0])
                print(tem_limit)
                if self.pot == 4:
                    sql1 += " and tem > %s;"
                    cur.execute(sql1, (s_datetime_sql, e_datetime_sql, tem_limit))
                    result = cur.fetchall()
                    # print (self.pot)

                else:
                    sql2 += " and tem > %s;"
                    cur.execute(sql2, (self.pot, s_datetime_sql, e_datetime_sql, tem_limit))
                    result = cur.fetchall()
                    # print (self.pot)


            else:
                if self.pot == 4:
                    sql1 += ";"
                    cur.execute(sql1, (s_datetime_sql, e_datetime_sql))
                    result = cur.fetchall()
                    # print (self.pot)

                else:
                    sql2 += ";"
                    cur.execute(sql2, (self.pot, s_datetime_sql, e_datetime_sql))
                    result = cur.fetchall()
                    # print (self.pot)


            # 关闭数据库连接
            cur.close()
            conn.close()
            # 判断结果集是否为空，如果为空，说明没有匹配的记录，返回False；否则，返回True
            if len(result) == 0:
                self.ui.sql_table_show.clear()
                QtWidgets.QMessageBox.warning(self, '错误', '未找到数据!')
            else:
                col_result = cur.description
                # 取得记录个数，用于设置表格的行数
                self.row = cur.rowcount  
                # 取得字段数，用于设置表格的列数
                self.vol = len(result[0])  
                col_result = list(col_result)
                a = 0
                self.ui.sql_table_show.setColumnCount(self.vol)
                self.ui.sql_table_show.setRowCount(self.row)
                #设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
                for i in col_result:   
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.sql_table_show.setHorizontalHeaderItem(a,item)
                    item = self.ui.sql_table_show.horizontalHeaderItem(a)
                    col_name = ["采样时间", "温度", "数据来源"]
                    item.setText(self._translate("Form", col_name[a]))
                    a = a + 1      

                result = list(result)     
                #将相关的数据
                for i in range(len(result)):      
                    #将获取的数据转为列表形式
                    result[i] = list(result[i])  
                for i in range(self.row):
                    for j in range(self.vol):
                        self.Table_Data(i,j,result[i][j])
                
                # 调整列和行的大小
                self.ui.sql_table_show.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                self.ui.sql_table_show.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
            
        else:
            self.ui.sql_table_show.clear()
            QtWidgets.QMessageBox.warning(self, '错误', '请先设置需要查询的罐子编号和临界温度!')



if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Ui_search_form()
    demo.show()
    sys.exit(app.exec_())