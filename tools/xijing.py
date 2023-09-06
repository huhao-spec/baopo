import os
import sys
# from predict import predict_1
from PyQt5 import QtCore
from PyQt5.QtWidgets import *
import time
from PyQt5.QtCore import *
from PyQt5.QtGui import *

i = -1
sec = -1


class WorkThread(QThread):
    timer = pyqtSignal()  # 每隔一秒发送信号
    end = pyqtSignal()  # 计数完成后发送一次信号

    def run(self):
        while True:
            time.sleep(0.5)  # 休眠1s
            if sec == 19999:
                self.end.emit()  # 发送end信号
                break
            self.timer.emit()  # 发送timer信号


class table(QMainWindow):
    def __init__(self):
        super(table, self).__init__()
        self.setWindowTitle('析晶系统')
        # 设置窗口长与宽
        screen = QDesktopWidget().screenGeometry()
        width = screen.width()
        height = screen.height()
        self.resize(800, 800)
        self.move(0, 0)
        self.num = 0
        layout = QVBoxLayout()
        self.tableWidget = QTableWidget()
        # 设置4行
        self.tableWidget.setRowCount(5)
        # 20000列
        self.tableWidget.setColumnCount(20000)
        # predioct()
        # 调整列与行,根据具体内容来设置
        # self.tableWidget.resizeColumnToContents()
        # self.tableWidget.resizeRowToContents()
        # 设置表头专属的列名子
        self.tableWidget.setVerticalHeaderLabels(["图片名字", "时间", "温度", "分类", "图片"])
        layout.addWidget(self.tableWidget)

        self.WorkThread = WorkThread()

        button1 = QPushButton('开始')
        layout.addWidget(button1)

        button2 = QPushButton('结束')
        layout.addWidget(button2)

        button1.clicked.connect(self.worker)
        button2.clicked.connect(self.end)


        # 禁止编辑
        self.tableWidget.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # 线程方法
        self.WorkThread.timer.connect(self.start)
        self.WorkThread.end.connect(self.end)
        mainFrame = QWidget()
        mainFrame.setLayout(layout)
        # 让窗口充满屏幕
        self.setCentralWidget(mainFrame)

    def start(self):
        # 循环条件；
        global sec
        sec += 1
        # 添加图片名字；强制转换i的数据类型，使之可自增
        global i
        i = int(i)
        i += 1
        item_int = QTableWidgetItem()
        i = str(sec)
        item_int.setText(i + ".png")
        self.tableWidget.setItem(0, sec, item_int)

        # 获取当前时间,并添加
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString('HH:mm:ss')
        self.tableWidget.setItem(1, sec, QTableWidgetItem(text))

        # 获取图片位置及把图片设置为icon
        read_image = ("D:/__easyHelper__/22")
        path_list = os.listdir(read_image)
        path_list.sort(key=lambda x: int(x[:-4]))
        filename = path_list[self.num]

        self.num += 1
        if self.num <= len(path_list):
            self.qweqwe = (read_image + "/" + filename)
            print(self.qweqwe)
            #predict_1(self.qweqwe)

            # self.tableWidget.setItem(3, sec, item_img)
            item_img = QTableWidgetItem()
            icon = QIcon(self.qweqwe)
            item_img.setIcon(QIcon(icon))
            self.tableWidget.setItem(4, sec, item_img)


    def worker(self):
        self.WorkThread.start()

    def end(self):
        QMessageBox.information(self, '消息', '计时结束')
        global sec
        sec = 19998



if __name__ == '__main__':
    app = QApplication(sys.argv)
    main = table()
    main.show()
    sys.exit(app.exec_())
