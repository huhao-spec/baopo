import sys
from PyQt5.QtCore import QDate,QDateTime,QTime
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import time
 
class DateTimeEditDemo(QWidget):
    def __init__(self):
        super(DateTimeEditDemo, self).__init__()
        self.initUI()
 
    def initUI(self):
        #设置标题与初始大小
        self.setWindowTitle('镇海危化品车查询')
        self.resize(500,380)
 
        #垂直布局/水平布局 QVBoxLayout/QHBoxLayout
        layout=QVBoxLayout()
        self.setLayout(layout) 
 
        #创建第一个日期时间空间,并把当前日期时间赋值,并修改显示格式
        self.label1 = QLabel('开始时间')
        self.dateEdit1=QDateTimeEdit(QDateTime.currentDateTime(),self)
        self.dateEdit1.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
 
        #设置第一个日期最大值与最小值，在当前日期的基础上，后一年与前一年
        self.dateEdit1.setMinimumDate(QDate.currentDate().addDays(-365))
        self.dateEdit1.setMaximumDate(QDate.currentDate().addDays(365))
 
        #设置第一个日历控件允许弹出
        self.dateEdit1.setCalendarPopup(True)
        self.label2 = QLabel('结束时间')
        #创建第二个日期时间空间，并把当前日期时间赋值，。并修改显示格式
        self.dateEdit2=QDateTimeEdit(QDateTime.currentDateTime(),self)
        self.dateEdit2.setDisplayFormat('yyyy-MM-dd HH:mm:ss')
 
        #设置第二个日期最大值与最小值，在当前日期的基础上，后一年与前一年
        self.dateEdit2.setMinimumDate(QDate.currentDate().addDays(-365))
        self.dateEdit2.setMaximumDate(QDate.currentDate().addDays(365))
 
        #设置第二个日历控件允许弹出
        self.dateEdit2.setCalendarPopup(True)
 
        #创建按钮并绑定一个自定义槽函数
        self.btn=QPushButton('点击查询')
        self.btn.clicked.connect(self.onButtonClick)
		
        #创建文本框用于显示想要输出的内容
        self.textEdit = QTextEdit()  
 
        #布局控件的加载与设置,可加载多个控件
        layout.addWidget(self.label1)
        layout.addWidget(self.dateEdit1)
        layout.addWidget(self.label2)
        layout.addWidget(self.dateEdit2)
        layout.addWidget(self.btn)
        layout.addWidget(self.textEdit)
 
    def onButtonClick(self):
        
        #dateTime是QDateTimeEdit的一个方法，返回QDateTime时间格式
        #需要再用toPyDateTime转变回python的时间格式
        dateTime1=str(self.dateEdit1.dateTime().toPyDateTime())[0:19]
        dateTime2=str(self.dateEdit2.dateTime().toPyDateTime())[0:19]
        
        #python时间格式转换
        n_time11 = time.strptime(dateTime1, "%Y-%m-%d %H:%M:%S")
        n_time22 = time.strptime(dateTime2, "%Y-%m-%d %H:%M:%S")
        n_time1 = int(time.strftime('%Y%m%d%H%M%S',n_time11))
        n_time2 = int(time.strftime('%Y%m%d%H%M%S',n_time22))
 
        self.textEdit.setText("This is pyqt's test!")
 
#if __name__ == '__main__'的作用是为了防止其他脚本只是调用该类时才开始加载，优化内存使用
if __name__ == '__main__':
    #调用
    app=QApplication(sys.argv)
    demo=DateTimeEditDemo()
    demo.show()
    sys.exit(app.exec_())