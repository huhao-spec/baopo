import datetime
import json
import random
import string
import sys
import time
from data_searching import Ui_MainWindow as Ui_Form
from model_mobile_net import efficientnet_b0 as create_model
import cv2
import pymysql
import pyqtgraph as pg
import torch
from PIL import Image
from torchvision import transforms
from Snap7.pySnap7 import Smart200
from welcome import *
from login import *
from interface import *
from data_searching_new import *
from camera import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow, QHeaderView
from PyQt5.QtGui import QPixmap, QImage, QColor
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer, QDateTime

from docx import Document
import pandas as pd


#pip freeze > requirements.txt
user_now = ''#当前用
cameras = ""#摄像头频道
crystal =  "" #结晶状态
temperature = ''#温度
account = ""#用户复写
pot = int(0) #罐子编号
id_user = int(0)#用户类型1管理员2普通用户
auto_cx =int(0)#自动冲洗
jiance =int(0)#

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

class CameraWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.init_plot()
        # 创建一个定时器，每隔1秒触发一次
        self.timer = QTimer()
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_data)
        # 启动定时器
        self.timer.start()
        # 连接到mysql数据库

        self.start_time = ""
        self.end_time = ""

        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # self.ui.pushButton.clicked.connect(self.log_out)
        # self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        #模拟输入
        # 创建1个 QTimer计时器对象
        timer = QtCore.QTimer(self)
        # 发射timeout信号，与自定义槽函数关联
        timer.timeout.connect(self.showtime)
        # 启动计时器
        timer.start()

        #模拟
        crystal = ""
        #----------------------------------------------------------------
        self.ui.lineEdit_camera.setText(cameras)
        self.ui.lineEdit_jj.setText(crystal)

        """ create model """
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
        self.model = create_model(num_classes=3).to(self.device)
        model_weight_path = "D:/undergrate_project/rongyexijing/weights/0.997.pth"
        self.model.load_state_dict(torch.load(model_weight_path, map_location=self.device))
        self.model.eval()
        json_path = 'class_indices.json'
        with open(json_path, "r") as f:
            self.class_indict = json.load(f)
        """ 界面 """
        # 创建 QLabel 控件用于显示图像
        self.image_label = QLabel()
        self.update_frame()
        self.ui.pushButton_end.clicked.connect(self.goreturn)

        self.show()

        # 设置进度条文字格式
        self.ui.progressBar_yr.setFormat('预热中 %p%'.format(self.ui.progressBar_yr.value() - self.ui.progressBar_yr.minimum()))
        self.ui.progressBar_start.setFormat('检测中 %p%'.format(self.ui.progressBar_start.value() - self.ui.progressBar_start.minimum()))
        self.ui.progressBar_cx.setFormat('冲洗中 %p%'.format(self.ui.progressBar_cx.value() - self.ui.progressBar_cx.minimum()))
        #预热进度条

        self.ui.progressBar_yr.setMinimum(0)
        self.ui.progressBar_yr.setMaximum(30)
        self.ui.progressBar_yr.setValue(0)
        self.ui.pushButton_start.clicked.connect(self.startCountdown_yr)
        
        self.timer0 = QTimer()
        self.timer0.setInterval(1000)  # 1秒钟更新一次
        self.timer0.timeout.connect(self.updateProgress1)

        #按下开始按钮后开始进度条
        self.ui.progressBar_start.setMinimum(0)
        self.ui.progressBar_start.setMaximum(720)
        self.ui.progressBar_start.setValue(0)

        self.timer1 = QTimer()
        self.timer1.setInterval(1000)  # 1秒钟更新一次
        self.timer1.timeout.connect(self.updateProgress2)

        #按下冲洗按钮后冲洗进度条
        self.ui.progressBar_cx.setMinimum(0)
        self.ui.progressBar_cx.setMaximum(30)
        self.ui.progressBar_cx.setValue(0)
        self.ui.pushButton_wash.clicked.connect(self.startCountdown_wash)
        self.timer2 = QTimer()
        self.timer2.setInterval(1000)  # 1秒钟更新一次
        self.timer2.timeout.connect(self.updateProgress3)

        self.timer3 = QTimer()
        self.timer3.setInterval(1000)  # 1秒钟更新一次
        self.timer3.timeout.connect(self.auto)
        self.ui.label_cameratime.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_cameratime.setScaledContents(True)

        self.timer_jilu = QTimer()
        self.timer_jilu.setInterval(1000)
        self.timer_jilu.timeout.connect(self.jilu_dingshi())


    def update_frame(self):
        self.main_time = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())
        url = 'rtsp://admin:a12345678@192.168.2.3'
        # 调用定时器更摄像头
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        self.camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
        video_name = 'D:/BaiduNetdiskDownload/2/' + str(datetime.date.today()) + '.avi'

        self.out = cv2.VideoWriter(video_name, fourcc, 20, (640, 480))

        self.timer_suanfa = QTimer(self)
        self.c_int = 0
        self.timer_suanfa.timeout.connect(self.update_img)
        self.timer_suanfa.start()

    def update_img(self):


        # 传入温度
        self.tem  = self.read_f(56, 57, 58, 59)
        # text = '温度为：'+tem
        text = "ceshi"
        # 摄像头更新实现函数
        ret, self.frame = self.camera.read()  # 读取摄像头帧
        frame = cv2.putText(self.frame, text, (200, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        self.out.write(frame)
        self.c_int += 1
        if ret:
            # 转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.ui.label_cameratime.setPixmap(pixmap)
            print(self.timer0.isActive(),self.timer1.isActive(),self.timer2.isActive(),self.timer3.isActive())
            if self.timer1.isActive():

                # 调用深度学习检测
                with torch.no_grad():
                    img = Image.fromarray(frame.astype('uint8')).convert('RGB')
                    data_transform = transforms.Compose(
                        [transforms.Resize(224),
                         transforms.CenterCrop(224),
                         transforms.ToTensor(),
                         transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
                    # [N, C, H, W]
                    img = data_transform(img)
                    img = torch.unsqueeze(img, dim=0)
                    # predict class
                    output = torch.squeeze(self.model(img.to(self.device))).cpu()
                    predict = torch.softmax(output, dim=0)
                    predict_cla = torch.argmax(predict).numpy()
                print_res = "class: {}".format(self.class_indict[str(predict_cla)])
                crystal_jieguo = str(print_res)
                self.ui.lineEdit_jj.setText(crystal_jieguo)
                if(predict_cla == 1):
                    self.timer_jilu.start()

            # create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            # db = database_connect()
            # cursor = db.cursor()
            # sql = "INSERT INTO tempurter (main_time, tem, pot_num) VALUES ('%s', %s, 1)" % (create_time, tem)
            # cursor.execute(sql)
            # db.commit()     # 需要获取到毫秒级时间，或者拿到一秒的延迟插入

    def jilu_dingshi(self):
        global jiange
        jiange = jiange + 1
        if (jiange == 10):
            jiange = 0
            self.timer_jilu.stop()
            self.jilu_caozuo()

    def jilu_caozuo(self):
        self.plc.WriteData('VB', 20, 0)
        img_name = 'D:/BaiduNetdiskDownload/2/' + str(datetime.date.today()) + '.jpg'
        cv2.imwrite(img_name, self.frame)

    def read_f(self, data1_int, data2_int, data3_int, data4_int):
        # 读数
        plc_read = Smart200('192.168.2.1')
        plc_read.ConnectPLC()
        data1_ori = plc_read.ReadData('VB', data1_int)
        data2_ori = plc_read.ReadData('VB', data2_int)
        data3_ori = plc_read.ReadData('VB', data3_int)
        data4_ori = plc_read.ReadData('VB', data4_int)
        # print(data1_ori)       # 取数
        data1_data = data1_ori['data']
        data2_data = data2_ori['data']
        data3_data = data3_ori['data']
        data4_data = data4_ori['data']
        # 变类型
        data1 = int(''.join(map(str, data1_data)))
        data2 = int(''.join(map(str, data2_data)))
        data3 = int(''.join(map(str, data3_data)))
        data4 = int(''.join(map(str, data4_data)))
        # 转转
        data = (data1 << 24) | (data2 << 16) | (data3 << 8) | data4

        if data & 0x80000000 > 0:
            nSign = -1
        else:
            nSign = 1

        nExp = data & 0x7F800000
        nExp = nExp >> 23
        nMantissa = data & 0x7FFFFF

        if nMantissa != 0:
            nMantissa = 1 + nMantissa / 8388608

        value = nSign * nMantissa * (2 ** (nExp - 127))
        value = str(value)
        return value

    def auto(self):
        global auto_cx
        # print(auto_cx)
        auto_cx = auto_cx +1 
        if(auto_cx==30):
            auto_cx = 0
            self.timer3.stop()
            self.timer2.start()

    def startCountdown_yr(self):
        # self.ui.progressBar_start.setValue(0)
        self.timer0.start()
        self.start_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    def startCountdown_wash(self):
        # self.ui.progressBar_cx.setValue(0)
        self.timer2.start()

    def updateProgress3(self):
        self.ui.progressBar_start.setValue(720)
        self.timer1.stop()
        self.ui.progressBar_yr.setValue(30)
        self.timer0.stop()
        value_wash = self.ui.progressBar_cx.value() + 1
        self.ui.progressBar_cx.setValue(value_wash)
        self.ui.lineEdit_jj.setText("检测结束")
        if value_wash == 30:
            self.timer2.stop()

    def updateProgress2(self):
        # print(self.ui.progressBar_start.value())
        value_start = self.ui.progressBar_start.value() + 1
        self.ui.progressBar_start.setValue(value_start)
        if value_start == 720:
            self.timer1.stop()
            self.timer3.start()

    def updateProgress1(self):
        value_yr = self.ui.progressBar_yr.value() + 1
        self.ui.progressBar_yr.setValue(value_yr)
        if value_yr == 15:
            PH =
            sql = "INSERT INTO ph_density_info (main_time, PH, Density, pot_name) VALUES ('%s', %s, %s, %d)" % (self.main_time, PH, Density, 1)
        if value_yr == 30:  # 预热操作 30s
            self.timer0.stop()
            self.timer1.start()

    def call_other_hide(self):
        self.win.ui.pushButton_manage.hide()

    def call_other_show(self):
        self.win.ui.pushButton_manage.show()

    def init_plot(self):
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle("近1分钟温度数据折线图")
        self.plotWidget.setLabel("left", "温度", "℃")
        self.plotWidget.setLabel("bottom", "时间","s")
        self.plotWidget.setRange(xRange=[0, 60], yRange=[40, 150])
        self.plotWidget.setBackground((245,245,220))
        self.ui.verticalLayout_qx.addWidget(self.plotWidget)
        # 创建一个空的数据列表，用于存储动态数据
        self.data = []
        # 创建一个曲线对象，用于绘制数据
        self.curve = self.plotWidget.plot(pen=pg.mkPen(color='blue', width=2))

    def update_data(self):
        conn = database_connect()
        cur = conn.cursor()
        # 从mysql数据库中读取最新的数据
        sql = "SELECT tem FROM tempurter where pot_num = " + str(pot) + " ORDER BY main_time DESC LIMIT 1;"
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 获取查询结果
            result = cur.fetchone()[0]
            cur.close()
            conn.close()
            if result:
                self.data.append(float(result))

                if len(self.data) > 60:
                    self.data.pop(0)

                # 更新曲线对象的数据
                self.curve.setData(self.data)
                self.ui.lineEdit_tem.setText(result)
        except Exception as e:
            # 如果发生错误，打印错误信息
            print(e)

        conn = database_connect()
        cur = conn.cursor()

        # 从mysql数据库中读取最新的数据
        sql = "SELECT PH FROM ph_density_info where pot_num = " + str(pot) + " ORDER BY main_time DESC LIMIT 1;"
        # 执行SQL语句
        cur.execute(sql)
        # 获取查询结果
        PH = cur.fetchone()[0]
        self.ui.lineEdit_ph.setText(PH)

        # 从mysql数据库中读取最新的数据
        sql = "SELECT Density FROM ph_density_info where pot_num = " + str(pot) + " ORDER BY main_time DESC LIMIT 1;"
        # 执行SQL语句
        cur.execute(sql)
        # 获取查询结果
        Density = cur.fetchone()[0]
        cur.close()
        conn.close()
        self.ui.lineEdit_density.setText(Density)

    def create_report(self):
        self.end_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        path = "../report/"+ self.end_time.replace(":", "_") + "检测报告.docx"

    # 自定义槽函数，用来在状态栏中显示当前日期时间
    def showtime(self):

        # 获取当前日期时间
        datetime = QtCore.QDateTime.currentDateTime()
        self.ui.lineEdit_time.clear()
        # 格式化日期时间
        text = datetime.toString('HH:mm:ss')
        self.ui.lineEdit_time.setText(text)

    def goreturn(self):
        self.win = Interfacepro()
        if account == '1':
            self.call_other_show()
        else:
            self.call_other_hide()

        cameras = ""
        self.timer_suanfa.stop()
        self.win.hide()
        self.win.show()
        self.close()
        self.camera.release()
        self.out.release()


    def log_out(self):
        self.close()
        self.login = LoginWindow()
        user_now = ''
        cameras = ""


     # 2.拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def toggle_fullscreen(self):
        if self.isFullScreen():  # 如果当前是全屏状态，则切换为普通窗口
            self.setWindowState(QtCore.Qt.WindowNoState)
        else:  # 如果当前是普通窗口，则切换为全屏
            self.setWindowState(QtCore.Qt.WindowFullScreen)

class welcome(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_welcome()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        ## 设置进度条文字格式
        self.ui.progressBar.setFormat(
            'Loaded %p%'.format(self.ui.progressBar.value() - self.ui.progressBar.minimum()))
        # 预热进度条
        self.ui.progressBar.setMinimum(0)
        self.ui.progressBar.setMaximum(100)
        self.ui.progressBar.setValue(0)
        self.timer = QTimer()
        self.timer.setInterval(5)  # 1秒钟更新一次
        self.timer.timeout.connect(self.updateProgress1)
        self.timer.start()
        self.win=Interfacepro()
    def updateProgress1(self):
        global id_user
        value = self.ui.progressBar.value() + 1
        self.ui.progressBar.setValue(value)
        if value == 100:  # 计时
            self.timer.stop()
            self.close()
            if id_user==int(1):
                self.win.show()
                self.win.ui.pushButton_manage.show()
            elif id_user==int(2):
                self.win.show()
                self.win.ui.pushButton_manage.hide()    

class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ui.widget_2.hide()

        def change_widget4():
            self.ui.widget_2.hide()
            self.ui.widget_4.show()

        def change_widget2():
            self.ui.widget_4.hide()
            self.ui.widget_2.show()

        self.ui.pushButton.clicked.connect(change_widget2)
        self.ui.pushButton_2.clicked.connect(change_widget4)


        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_3.clicked.connect(self.go_to_inter)
        self.ui.pushButton_6.clicked.connect(self.go_to_inter_manage)
        # 连接复选框的状态变化信号到槽函数
        self.ui.checkBox.stateChanged.connect(self.on_state_changed)
        #self.win = InterfaceWindow()
        # self.win = Interfacepro()
        self.show()
        # 创建OtherClass实例对象

    # def call_other_hide(self):
    #     self.win.ui.pushButton_manage.hide()
    #
    # def call_other_show(self):
    #     self.win.ui.pushButton_manage.show()

    def on_state_changed(self, state):
        if state == 2:  # Qt.Checked
            self.ui.lineEdit.setText(account)
    # 管理员登录
    def go_to_inter_manage(self):
        global account
        global id_user
        account = self.ui.lineEdit_4.text()
        password = self.ui.lineEdit_5.text()
        flag = self.admin_check(account, password)
        if flag:
            self.win_welcome = welcome()
            id_user=int(1)
            # self.win.hide()
            self.win_welcome.show()
            # self.win.show()
            # self.call_other_show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Invalid username or password')
    # 普通用户登录
    def go_to_inter(self):
        global account
        global id_user
        account = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        flag = self.nomal_usr_check(account, password)
        if flag:
            self.win_welcome = welcome()
            id_user=int(2)
            # self.win.hide()
            self.win_welcome.show()
            # self.win.show()
            # self.call_other_hide()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Invalid username or password')
        
    # 2.拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def nomal_usr_check(self, username, password):
        # 连接sqlite数据库，并执行查询语句，获取最新的数据
        conn = database_connect()
        cur = conn.cursor()
        # 构造查询语句，根据username和password查找usr表中的记录
        sql = "SELECT * FROM user_info WHERE usr_name = %s AND usr_pass = %s;"
        # 执行查询语句，并获取结果集
        cur.execute(sql, (username, password))
        result = cur.fetchall()
        # 关闭数据库连接
        cur.close()
        conn.close()
        # 判断结果集是否为空，如果为空，说明没有匹配的记录，返回False；否则，返回True
        if len(result) == 0:
            return False
        else:
            return True

    def admin_check(self, username, password):
        # 连接sqlite数据库，并执行查询语句，获取最新的数据
        conn = database_connect()
        cur = conn.cursor()
        # 构造查询语句，根据username和password查找usr表中的记录
        sql = "SELECT * FROM admin_info WHERE admin_name = %s AND admin_pass = %s;"
        # 执行查询语句，并获取结果集
        cur.execute(sql, (username, password))
        result = cur.fetchall()
        # 关闭数据库连接
        cur.close()
        conn.close()
        # 判断结果集是否为空，如果为空，说明没有匹配的记录，返回False；否则，返回True
        if len(result) == 0:
            return False
        else:
            return True

class Interfacepro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2pro()
        self.ui.setupUi(self)
        self._translate = QtCore.QCoreApplication.translate
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_return1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_return.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_ch_decode.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_manage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))
        
        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_find.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_delete.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))
        self.ui.action105A.triggered.connect(self.go_to_inter1)
        self.ui.action105B.triggered.connect(self.go_to_inter2)
        self.ui.action102.triggered.connect(self.go_to_inter3)
        self.ui.actionexit.triggered.connect(self.close)
        self.ui.actionlogout.triggered.connect(self.log_out)
        self.ui.action_searching.triggered.connect(self.go_to_data_search)
        # self.ui.action_about.triggered.connect()

        #调用本地摄像头
        self.update_frame_105a()

        # 设置 QLabel 的大小策略为 Expanding
        self.ui.label_v1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v1.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中

        self.ui.label_v2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v2.setScaledContents(True)

        self.ui.label_v3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v3.setScaledContents(True)
        # -------------------------------------------------------------------------------------------
        # self.ui.pushButton.clicked.connect(self.log_out)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_v1.clicked.connect(self.go_to_inter1)
        self.ui.pushButton_v2.clicked.connect(self.go_to_inter2)
        self.ui.pushButton_v3.clicked.connect(self.go_to_inter3)
        # self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        self.ui.pushButton_record.clicked.connect(self.go_to_data_search)
        self.ui.pushButton_change.clicked.connect(self.admin_pass_change)
        self.ui.pushButton_affirmregister.clicked.connect(self.user_reg)
        self.ui.pushButton_find_all.clicked.connect(self.user_searching)
        self.ui.ori_delete.clicked.connect(self.user_delete_check)

    def admin_pass_change(self):  
        ori_pwd = self.ui.lineEdit_pass.text()
        conn = database_connect()
        cur = conn.cursor()
        sql = "select admin_pass FROM admin_info;"
        try:
            cur.execute(sql)
        except:
            print('SQL执行失败,执行语句为:%s'%str(sql))

        admin_pwd = cur.fetchall()[0][0]

        if(admin_pwd != ori_pwd):
            QtWidgets.QMessageBox.warning(self, '错误', '原始密码错误!')
        else:
            if (self.ui.lineEdit_newpass1.text() != self.ui.lineEdit_newpass2.text()):
                QtWidgets.QMessageBox.warning(self, '错误', '两次密码输入不一致!')
            else:
                conn = database_connect()
                cur = conn.cursor()
                sql = "UPDATE admin_info SET admin_pass = %s;"
                try:
                    cur.execute(sql,(self.ui.lineEdit_newpass1.text()))
                    conn.commit()
                    cur.close()
                    conn.close()
                    QtWidgets.QMessageBox.warning(self, '完成', '修改完成!')
                except:
                    print('SQL执行失败,执行语句为:%s'%str(sql))

 
    def user_reg(self):
        if(len(self.ui.lineEdit_decode.text()) != 0 and len(self.ui.lineEdit_AffirmDecode.text() != 0)):
            if (self.ui.lineEdit_decode.text() != self.ui.lineEdit_AffirmDecode.text()):
                QtWidgets.QMessageBox.warning(self, '错误', '两次密码输入不一致!')
            else:
                conn = database_connect()
                cur = conn.cursor()
                while(1):
                    uid = "".join(map(lambda x:random.choice(string.digits), range(8)))
                    
                    sql = "select usr_name FROM user_info where usr_id = %s;"
                    try:
                        cur.execute(sql,(uid))
                        result = cur.fetchall()
                        if len(result) == 0:
                            break
                    except:
                        print('SQL执行失败,执行语句为:%s'%str(sql))

                sql = "INSERT INTO user_info VALUES(%s, %s, %s);"
                try:
                        cur.execute(sql,(uid, self.ui.lineEdit_register.text(), self.ui.lineEdit_decode.text()))
                        conn.commit()
                        QtWidgets.QMessageBox.warning(self, '完成', '注册成功!')
                except:
                    print('SQL执行失败,执行语句为:%s'%str(sql))
                cur.close()
                conn.close()
        
        else:
            QtWidgets.QMessageBox.warning(self, '错误', '用户名或密码为空!')

    def user_searching(self):
        user_name = self.ui.lineEdit_find.text()
        conn = database_connect()
        cur = conn.cursor()
        try:
            sql = "select * FROM user_info where usr_name = %s;"
            cur.execute(sql, (user_name))
            result = cur.fetchall()
            cur.close()
            conn.close()
        except Exception as e:
                # 如果发生错误，打印错误信息
                print(e)

        if len(result) == 0:
            self.ui.find_result.clear()
            QtWidgets.QMessageBox.warning(self, '错误', '未找到用户信息!')
        
        else:
            
            col_result = cur.description
            # 取得记录个数，用于设置表格的行数
            self.row = cur.rowcount  
            # 取得字段数，用于设置表格的列数
            self.vol = len(result[0])  
            col_result = list(col_result)
            a = 0
            self.ui.find_result.setColumnCount(self.vol)
            self.ui.find_result.setRowCount(self.row)
            #设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
            for i in col_result:   
                item = QtWidgets.QTableWidgetItem()
                self.ui.find_result.setHorizontalHeaderItem(a,item)
                item = self.ui.find_result.horizontalHeaderItem(a)
                col_name = ["用户id", "用户名", "用户密码"]
                item.setText(self._translate("Form", col_name[a]))
                a = a + 1      

            result = list(result)     
            #将相关的数据
            for i in range(len(result)):      
                #将获取的数据转为列表形式
                result[i] = list(result[i])  
            for i in range(self.row):
                for j in range(self.vol):
                    item = QtWidgets.QTableWidgetItem()
                    self.ui.find_result.setItem(i,j, item)
                    item = self.ui.find_result.item(i,j)
                    item.setText(self._translate("Form", str(result[i][j])))
            
            # 调整列和行的大小
            self.ui.find_result.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
            # self.ui.find_result.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
    
    def user_delete_check(self):
        if (self.ui.lineEdit_delete.text() != self.ui.lineEdit_affirmdelete.text()):
            QtWidgets.QMessageBox.warning(self, '错误', '请确认两次输入相同用户id!')

        else:
            conn = database_connect()
            cur = conn.cursor()
            try:
                sql = "select * FROM user_info where usr_id = %s;"
                cur.execute(sql, (self.ui.lineEdit_delete.text()))
                result = cur.fetchall()
                cur.close()
                conn.close()
            except Exception as e:
                    # 如果发生错误，打印错误信息
                    print(e)

            if len(result) == 0:
                self.ui.delete_usr_info.clear()
                QtWidgets.QMessageBox.warning(self, '错误', '未找到用户信息!')
            else:
                conn = database_connect()
                cur = conn.cursor()
                sql = "select admin_pass FROM admin_info;"
                try:
                    cur.execute(sql)
                    cur.close()
                    conn.close()
                except:
                    print('SQL执行失败,执行语句为:%s'%str(sql))

                admin_pwd = cur.fetchall()[0][0]

                if(self.ui.lineEdit_managedecode.text() != admin_pwd):
                    QtWidgets.QMessageBox.warning(self, '错误', '管理员密码错误!')
                else:
                    conn = database_connect()
                    cur = conn.cursor()
                    try:
                        sql = "select * FROM user_info where usr_id = %s;"
                        cur.execute(sql, (self.ui.lineEdit_delete.text()))
                        result = cur.fetchall()
                        
                    except Exception as e:
                        # 如果发生错误，打印错误信息
                        print(e)
                    col_result = cur.description
                    
                    # 取得记录个数，用于设置表格的行数
                    self.row = cur.rowcount
                    # print(self.row)
                    # 取得字段数，用于设置表格的列数
                    self.vol = len(result[0])
                    # print(self.vol)
                    col_result = list(col_result)
                    a = 0
                    self.ui.delete_usr_info.setColumnCount(self.vol)
                    self.ui.delete_usr_info.setRowCount(self.row)
                    #设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
                    for i in col_result:
                        item = QtWidgets.QTableWidgetItem()
                        self.ui.delete_usr_info.setHorizontalHeaderItem(a,item)
                        item = self.ui.delete_usr_info.horizontalHeaderItem(a)
                        col_name = ["用户id", "用户名", "用户密码"]
                        item.setText(self._translate("Form", col_name[a]))
                        print(a)
                        a = a + 1

                result = list(result)
                #将相关的数据
                for i in range(len(result)):
                    #将获取的数据转为列表形式
                    result[i] = list(result[i])
                for i in range(self.row):
                    for j in range(self.vol):
                        item = QtWidgets.QTableWidgetItem()
                        self.ui.delete_usr_info.setItem(i, j, item)
                        item = self.ui.delete_usr_info.item(i,j)
                        item.setText(self._translate("Form", str(result[i][j])))

                # 调整列和行的大小
                self.ui.delete_usr_info.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
                # self.ui.delete_usr_info.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                cur.close()
                conn.close()
  
                conn = database_connect()
                cur = conn.cursor()
                try:
                    sql = "select * FROM user_info where usr_id = %s;"
                    cur.execute(sql, (self.ui.lineEdit_delete.text()))
                    conn.commit()
                    cur.close()
                    conn.close()
                    QtWidgets.QMessageBox.warning(self, '完成', '删除完成!')
                    
                except Exception as e:
                    # 如果发生错误，打印错误信息
                    print(e)

    def update_frame_105a(self):
        # mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        #url = 'rtsp://admin:a12345678@192.168.2.3'
        self.camera = cv2.VideoCapture(0)
        self.timer_jiemian = QTimer(self)
        self.timer_jiemian.start()
        self.timer_jiemian.timeout.connect(self.update_img_105a)

    def update_img_105a(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString("yyyy年MM月dd日 hh:mm:ss")
        self.ui.label_time.setText("欢迎您:"+str(id_user)+" " + text)
        ret, frame = self.camera.read()  # 读取摄像头帧
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为RGB格式
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.ui.label_v1.setPixmap(pixmap)
            self.ui.label_v2.setPixmap(pixmap)
            self.ui.label_v3.setPixmap(pixmap)

    def showtime(self):
        datetime = QtCore.QDateTime.currentDateTime()
        text = datetime.toString("yyyy年MM月dd日 hh:mm:ss")
        self.ui.label_time.setText("欢迎您:"+str(id_user)+" " + text)
    def go_to_data_search(self):
        self.timer_jiemian.stop()
        self.close()
        self.dataui = Data_search()

    def go_to_inter1(self):
        self.timer_jiemian.stop()
        self.close()
        global cameras
        global pot
        cameras = "频道1"
        pot = 1
        self.login = CameraWindow()
    def go_to_inter2(self):
        self.timer_jiemian.stop()
        self.close()
        global cameras
        global pot
        cameras = "频道2"
        pot = 2
        self.login = CameraWindow()
    def go_to_inter3(self):
        self.timer_jiemian.stop()
        self.close()
        global cameras
        global pot
        cameras = "频道3"
        pot = 3
        self.login = CameraWindow()

    def log_out(self):
        self.timer_jiemian.stop()
        self.close()
        self.login = LoginWindow()
        user_now = ''

    # 2.拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def toggle_fullscreen(self):
        if self.isFullScreen():  # 如果当前是全屏状态，则切换为普通窗口
            self.setWindowState(QtCore.Qt.WindowNoState)
        else:  # 如果当前是普通窗口，则切换为全屏
            self.setWindowState(QtCore.Qt.WindowFullScreen)

class Data_search(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_Form()
        self.ui.setupUi(self)
        self.print_out_sql = ""
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        # self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._translate = QtCore.QCoreApplication.translate
        self.init_plot()
        self.buttom_set_flag = False
        self.pot = 1
        init_temlmt = self.temlmt_search()[0][0]
        self.ui.tem_limit.setValue(init_temlmt)
        self.ui.Confirm_button.clicked.connect(self.searching)
        self.ui.set_pot_lim_tem.clicked.connect(self.set_pot_lim_tem)
        self.ui.print_out.clicked.connect(self.print_out_xlsx)

        # self.ui.pushButton.clicked.connect(self.log_out)
        # self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        self.ui.pushButton_return.clicked.connect(self.goreturn)
        self.win = Interfacepro()
        if id_user==1:
            self.call_other_show()
        else:
            self.call_other_hide()
        self.show()

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
            cur.close()
            conn.close()
            return result

        except Exception as e:
            # 如果发生错误，打印错误信息
            print(e)

        

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

                    self.print_out_sql = "SELECT * FROM tempurter WHERE main_time between \""+ s_datetime_sql +"\" and \"" + e_datetime_sql + "\" and tem > " + str(tem_limit) + ";"
                    print(self.print_out_sql)

                    cur.execute(sql1, (s_datetime_sql, e_datetime_sql, tem_limit))
                    result = cur.fetchall()
                    # print (self.pot)
                

                else:
                    sql2 += " and tem > %s;"  

                    self.print_out_sql = "SELECT * FROM tempurter WHERE pot_num = "+ str(self.pot) +" and main_time between \""+ s_datetime_sql +"\" and \"" + e_datetime_sql + "\" and tem > " + str(tem_limit) + ";"
                    print(self.print_out_sql)
                    

                    cur.execute(sql2, (self.pot, s_datetime_sql, e_datetime_sql, tem_limit))
                    result = cur.fetchall()
                    # print (self.pot)
                
            else:
                if self.pot == 4:
                    sql1 += ";"

                    self.print_out_sql = "SELECT * FROM tempurter WHERE main_time between \""+ s_datetime_sql +"\" and \"" + e_datetime_sql + "\";"
                    print(self.print_out_sql)

                    cur.execute(sql1, (s_datetime_sql, e_datetime_sql))
                    result = cur.fetchall()
                    # print (self.pot)

                else:
                    sql2 += ";"

                    self.print_out_sql = "SELECT * FROM tempurter WHERE pot_num = "+ str(self.pot) +" and main_time between \""+ s_datetime_sql +"\" and \"" + e_datetime_sql + "\";"
                    print(self.print_out_sql)

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
                # self.ui.sql_table_show.verticalHeader().setSectionResizeMode(QHeaderView.Stretch)
                
            
        else:
            self.ui.sql_table_show.clear()
            QtWidgets.QMessageBox.warning(self, '错误', '请先设置需要查询的罐子编号和临界温度!')


    def print_out_xlsx(self):
        if(len(self.print_out_sql)!= 0):
            create_time = datetime.now().strftime("%Y-%m-%d %H_%M_%S")
            conn = database_connect()
            df = pd.read_sql(self.print_out_sql, con=conn)
            conn.close()
            file_name = "../data/" + create_time + ".xlsx"
            first_col = ["", "时间", "温度", "罐名称"]
            df.to_excel(file_name, index=False)
            
        else:
            QtWidgets.QMessageBox.warning(self, '错误', '请先查询后导出数据!')
        
    # def print_out(self):


    def goreturn(self):
        self.close()
        self.win.show()
        cameras = ""

    def call_other_hide(self):
        self.win.ui.pushButton_manage.hide()

    def call_other_show(self):
        self.win.ui.pushButton_manage.show()

    def log_out(self):
        self.close()
        self.login = LoginWindow()
        user_now = ''
        cameras = ""


     # 2.拖动
    def mousePressEvent(self, event):
        if event.button() == QtCore.Qt.LeftButton and self.isMaximized() == False:
            self.m_flag = True
            self.m_Position = event.globalPos() - self.pos()  # 获取鼠标相对窗口的位置
            event.accept()
            self.setCursor(QtGui.QCursor(QtCore.Qt.OpenHandCursor))  # 更改鼠标图标

    def mouseMoveEvent(self, mouse_event):
        if QtCore.Qt.LeftButton and self.m_flag:
            self.move(mouse_event.globalPos() - self.m_Position)  # 更改窗口位置
            mouse_event.accept()

    def mouseReleaseEvent(self, mouse_event):
        self.m_flag = False
        self.setCursor(QtGui.QCursor(QtCore.Qt.ArrowCursor))

    def toggle_fullscreen(self):
        if self.isFullScreen():  # 如果当前是全屏状态，则切换为普通窗口
            self.setWindowState(QtCore.Qt.WindowNoState)
        else:  # 如果当前是普通窗口，则切换为全屏
            self.setWindowState(QtCore.Qt.WindowFullScreen)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())