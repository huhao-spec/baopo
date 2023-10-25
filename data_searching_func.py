import sys
import time
import pymysql
import pyqtgraph as pg

from Ui_data_searching import Ui_Form
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow 
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
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
        self.ui.Confirm_button.clicked.connect(self.onButtonClick)

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
        item.setText(self._translate("Form", str(data)))

    def tem_limit_update(self):
        tem_limited = self.ui.tem_limit.text()
        conn = database_connect()
        cur = conn.cursor()
        sql = "replace into tempurter_limit(limit_level, tem_limit, pot_num) VALUES(%s, %s, %s);"
        cur.execute(sql, (s_datetime_sql, e_datetime_sql))

    def onButtonClick(self):
        
        #dateTime是QDateTimeEdit的一个方法，返回QDateTime时间格式
        #需要再用toPyDateTime转变回python的时间格式
        s_datetime=str(self.ui.s_datetime.dateTime().toPyDateTime())[0:19]
        e_datetime=str(self.ui.e_datetime.dateTime().toPyDateTime())[0:19]
        
        #mysql时间格式转换
        s_datetime_original = time.strptime(s_datetime, "%Y-%m-%d %H:%M:%S")
        s_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S',s_datetime_original)

        e_datetime_original = time.strptime(e_datetime, "%Y-%m-%d %H:%M:%S")
        e_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S',e_datetime_original)
        
        data_source = int(self.ui.data_source.currentIndex()) + 1

        conn = database_connect()
        cur = conn.cursor()
        try:
            if data_source == 4:
                sql = "SELECT * FROM tempurter WHERE main_time between %s and %s;"
                cur.execute(sql, (s_datetime_sql, e_datetime_sql))
                result = cur.fetchall()
                print (data_source)
            else:
                sql = "SELECT * FROM tempurter WHERE pot_num = %s and main_time between %s and %s;"
                cur.execute(sql, (data_source, s_datetime_sql, e_datetime_sql))
                result = cur.fetchall()
                print (data_source)
                
        except Exception as e:
            # 如果发生错误，打印错误信息
            print(e)

        # 关闭数据库连接
        cur.close()
        conn.close()
        # 判断结果集是否为空，如果为空，说明没有匹配的记录，返回False；否则，返回True
        if len(result) == 0:
            self.ui.sql_table_show.clear()
            QtWidgets.QMessageBox.warning(self, 'Error', 'data not found')
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
                item.setText(self._translate("Form", i[0]))
                a = a + 1

            # 将数据格式改为列表形式，其是将数据库中取出的数据整体改为列表形式
            result = list(result)          
            #将相关的数据
            for i in range(len(result)):      
                #将获取的数据转为列表形式
                result[i] = list(result[i])  
            for i in range(self.row):
                for j in range(self.vol):
                    self.Table_Data(i,j,result[i][j])

        

if __name__ == '__main__':
    app=QApplication(sys.argv)
    demo=Ui_search_form()
    demo.show()
    sys.exit(app.exec_())