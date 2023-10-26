import datetime
import json
import random
import struct
import sys
import time
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
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer, QDateTime

# pip freeze > requirements.txt
user_now = ''  # 当前用户
cameras = ""  # 摄像头频道
crystal = ""  # 结晶状态
temperature = ''  # 温度
account = ""  # 用户复写
pot = int(0)  # 罐子编号
id_user = int(0)  # 用户类型1管理员2普通用户


def database_connect():
    connect = pymysql.connect(
        host='127.0.0.1'
        , user='root'
        , passwd='123456'
        , port=3306
        , db='test_database'
        , charset='utf8'
    )
    return connect


class CameraWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        # self.plc = Smart200('192.168.2.1')
        # self.plc.ConnectPLC()
        # self.plc.WriteData('VB', 7.0, 3)
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.init_plot()
        # 创建一个定时器，每隔1秒触发一次
        self.timer_database = QTimer()
        self.timer_database.setInterval(1000)
        self.timer_database.timeout.connect(self.update_data)
        # 启动定时器
        self.timer_database.start()
        self.conn = database_connect()
        self.cursor = self.conn.cursor()
        # 连接到mysql数据库

        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        crystal = ""
        # ----------------------------------------------------------------
        self.ui.textBrowser_1.append(cameras)

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
        # 加载图像
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小

        image_label1 = QLabel()
        pixmap = QPixmap("test.jpg")
        image_label1.setPixmap(pixmap)
        image_label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label1.setScaledContents(True)

        # 将 QLabel 控件添加到布局中
        self.ui.verticalLayout_camera.addWidget(self.image_label)
        # ------------------------------------------------------------------------------------

        self.ui.pushButton_end.clicked.connect(self.goreturn)

        self.show()

        # 设置进度条文字格式
        self.ui.progressBar_yr.setFormat(
            '预热中 %p%'.format(self.ui.progressBar_yr.value() - self.ui.progressBar_yr.minimum()))
        self.ui.progressBar_start.setFormat(
            '检测中 %p%'.format(self.ui.progressBar_start.value() - self.ui.progressBar_start.minimum()))
        self.ui.progressBar_cx.setFormat(
            '冲洗中 %p%'.format(self.ui.progressBar_cx.value() - self.ui.progressBar_cx.minimum()))
        # 预热进度条

        self.ui.progressBar_yr.setMinimum(0)
        self.ui.progressBar_yr.setMaximum(120)
        self.ui.progressBar_yr.setValue(0)
        self.timer = QTimer()
        self.timer.setInterval(1000)  # 1秒钟更新一次
        self.timer.timeout.connect(self.updateProgress1)
        self.timer.start()

        # 按下开始按钮后开始进度条
        self.ui.progressBar_start.setMinimum(0)
        self.ui.progressBar_start.setMaximum(120)
        self.ui.progressBar_start.setValue(0)
        self.ui.pushButton_start.clicked.connect(self.startCountdown_start)
        self.timer1 = QTimer()
        self.timer1.setInterval(1000)  # 1秒钟更新一次
        self.timer1.timeout.connect(self.updateProgress2)

        # 按下冲洗按钮后冲洗进度条
        self.ui.progressBar_cx.setMinimum(0)
        self.ui.progressBar_cx.setMaximum(120)
        self.ui.progressBar_cx.setValue(0)
        self.ui.pushButton_wash.clicked.connect(self.startCountdown_wash)
        self.timer2 = QTimer()
        self.timer2.setInterval(1000)  # 1秒钟更新一次
        self.timer2.timeout.connect(self.updateProgress3)


    def update_frame(self):
        url = 'rtsp://admin:a12345678@192.168.2.3'
        # 调用定时器更摄像头
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        self.camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
        name = 'D:/BaiduNetdiskDownload/2/' + str(datetime.date.today()) + '.avi'
        self.out = cv2.VideoWriter(name, fourcc, 20, (640, 480))

        self.timer_suanfa = QTimer(self)
        self.c_int = 0
        self.timer_suanfa.timeout.connect(self.update_img)
        self.timer_suanfa.start()

    def update_img(self):
        # 写入时间
        datetime1 = QtCore.QDateTime.currentDateTime()
        self.ui.textBrowser_5.clear()
        text = datetime1.toString('HH:mm:ss')
        self.ui.textBrowser_5.append(text)

        # 传入温度
        # tem  = self.read_f(56, 57, 58, 59)
        # self.ui.textBrowser_3.clear()
        # self.ui.textBrowser_3.append(tem)

        # 传入密度3
        # midu = self.read_f(48, 49, 50, 51)
        # self.ui.textBrowser_4.clear()
        # self.ui.textBrowser_4.append(midu)

        # 传入ph4
        # ph = self.read_f(44, 45, 46, 47)
        # self.ui.textBrowser_5.clear()
        # self.ui.textBrowser_5.append(ph)

        # 摄像头更新实现函数
        ret, frame = self.camera.read()  # 读取摄像头帧
        frame = cv2.putText(frame, text, (200, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        self.out.write(frame)
        self.c_int += 1
        if ret:
            # 转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
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
                print(self.timer_suanfa.isActive())
                # if(print_res = kaishi):
                #     self.plc.WriteData('VB', 8, 1)
                crystal_jieguo = str(print_res)
                self.ui.textBrowser_2.clear()
                self.ui.textBrowser_2.append(crystal_jieguo)
            create_time = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')
            tem = "%.2f" % (random.random() + random.randint(20, 120))
            db = database_connect()
            cursor = db.cursor()
            sql = "INSERT INTO tempurter (main_time, tem, pot_num) VALUES ('%s', %s, 1)" % (create_time, tem)
            cursor.execute(sql)
            db.commit()     # 需要获取到毫秒级时间，或者拿到一秒的延迟插入


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

    def startCountdown_start(self):
        self.ui.progressBar_start.setValue(0)
        self.timer1.start()

    def startCountdown_wash(self):
        self.ui.progressBar_cx.setValue(0)
        self.timer2.start()

    def updateProgress3(self):
        value_wash = self.ui.progressBar_cx.value() + 1
        self.ui.progressBar_cx.setValue(value_wash)
        if value_wash == 0:
            self.timer2.stop()

    def updateProgress2(self):
        value_start = self.ui.progressBar_start.value() + 1
        self.ui.progressBar_start.setValue(value_start)
        if value_start == 0:
            self.timer1.stop()

    def updateProgress1(self):
        value_yr = self.ui.progressBar_yr.value() + 1
        self.ui.progressBar_yr.setValue(value_yr)
        if value_yr == 120:  # 计时2分钟
            self.timer.stop()

    def call_other_hide(self):
        self.win.ui.pushButton_manage.hide()

    def call_other_show(self):
        self.win.ui.pushButton_manage.show()

    def init_plot(self):
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle("实时数据折线图")
        self.plotWidget.setLabel("left", "数据值")
        self.plotWidget.setLabel("bottom", "时间", "s")
        self.plotWidget.setRange(xRange=[0, 60], yRange=[0, 150])
        self.ui.verticalLayout_qx.addWidget(self.plotWidget)

        # 创建一个空的数据列表，用于存储动态数据
        self.data = []

        # 创建一个曲线对象，用于绘制数据
        self.curve = self.plotWidget.plot(pen=pg.mkPen(color='y', width=2))

    def update_data(self):
        conn = database_connect()
        cur = conn.cursor()
        # 从mysql数据库中读取最新的数据
        sql = "SELECT tem FROM tempurter where pot_num = " + str(pot) + " ORDER BY main_time DESC LIMIT 1"
        try:
            # 执行SQL语句
            cur.execute(sql)
            # 获取查询结果
            result = cur.fetchone()[0]
            conn.close()
            if result:
                self.data.append(float(result))

                if len(self.data) > 60:
                    self.data.pop(0)

                # 更新曲线对象的数据
                self.curve.setData(self.data)
                self.ui.textBrowser_3.setText(result)
        except Exception as e:
            # 如果发生错误，打印错误信息
            print(e)

    # 自定义槽函数，用来在状态栏中显示当前日期时间
    def showtime(self):

        # 获取当前日期时间
        datetime = QtCore.QDateTime.currentDateTime()
        self.ui.textBrowser_5.clear()
        # 格式化日期时间
        text = datetime.toString('HH:mm:ss')
        self.ui.textBrowser_5.append(text)

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
        self.timer.setInterval(15)  # 1秒钟更新一次
        self.timer.timeout.connect(self.updateProgress1)
        self.timer.start()
        self.win = Interfacepro()

    def updateProgress1(self):
        global id_user
        value = self.ui.progressBar.value() + 1
        self.ui.progressBar.setValue(value)
        if value == 100:  # 计时
            self.timer.stop()
            self.close()
            if id_user == int(1):
                self.win.show()
                self.win.ui.pushButton_manage.show()
            elif id_user == int(2):
                self.win.show()
                self.win.ui.pushButton_manage.hide()


class LoginWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow1()
        self.ui.setupUi(self)
        self.ui.widget_4.hide()

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
        self.show()

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
            id_user = int(1)
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
            id_user = int(2)
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
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_return1.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_return.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_ch_decode.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_manage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_find.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_delete.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))

        self.update_frame_105a()
        # 设置 QLabel 的大小策略为 Expanding
        self.ui.label_v1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v1.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中

        # image_label1 = QLabel()

        self.ui.label_v2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v2.setScaledContents(True)

        # image_label2 = QLabel()

        self.ui.label_v3.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v3.setScaledContents(True)

        self.ui.horizontalLayout_v1.addWidget(self.ui.label_v1)
        self.ui.horizontalLayout_v2.addWidget(self.ui.label_v2)
        self.ui.horizontalLayout_v3.addWidget(self.ui.label_v3)
        # -------------------------------------------------------------------------------------------

        self.ui.pushButton.clicked.connect(self.log_out)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_v1.clicked.connect(self.go_to_inter1)
        self.ui.pushButton_v2.clicked.connect(self.go_to_inter2)
        self.ui.pushButton_v3.clicked.connect(self.go_to_inter3)

        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)

        self.ui.pushButton_record.clicked.connect(self.go_to_data_search)

    def update_frame_105a(self):
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        url = 'rtsp://admin:a12345678@192.168.2.3'
        self.camera = cv2.VideoCapture(0)
        self.timer_jiemian = QTimer(self)
        self.timer_jiemian.start()
        self.timer_jiemian.timeout.connect(self.update_img_105a)

    def update_img_105a(self):
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

    def go_to_data_search(self):
        # self.timer_suanfa.stop()
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
        self.ui = Ui_data_search()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)

        self._translate = QtCore.QCoreApplication.translate
        self.init_plot()
        self.ui.pushButton_tem.clicked.connect(self.onButtonClick)

        self.ui.pushButton.clicked.connect(self.log_out)
        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        self.ui.pushButton_return.clicked.connect(self.goreturn)
        self.win = Interfacepro()
        if id_user == 1:
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

    def Table_Data(self, i, j, data):

        item = QtWidgets.QTableWidgetItem()
        self.ui.sql_table_show.setItem(i, j, item)
        item = self.ui.sql_table_show.item(i, j)
        item.setText(self._translate("Form", str(data)))

    def tem_limit_update(self):
        tem_limited = self.ui.tem_limit.text()
        conn = database_connect()
        cur = conn.cursor()
        sql = "replace into tempurter_limit(limit_level, tem_limit, pot_num) VALUES(%s, %s, %s);"
        cur.execute(sql, (s_datetime_sql, e_datetime_sql))

    def onButtonClick(self):

        # dateTime是QDateTimeEdit的一个方法，返回QDateTime时间格式
        # 需要再用toPyDateTime转变回python的时间格式
        s_datetime = str(self.ui.s_datetime.dateTime().toPyDateTime())[0:19]
        e_datetime = str(self.ui.e_datetime.dateTime().toPyDateTime())[0:19]

        # mysql时间格式转换
        s_datetime_original = time.strptime(s_datetime, "%Y-%m-%d %H:%M:%S")
        s_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S', s_datetime_original)

        e_datetime_original = time.strptime(e_datetime, "%Y-%m-%d %H:%M:%S")
        e_datetime_sql = time.strftime('%Y-%m-%d %H:%M:%S', e_datetime_original)

        data_source = int(self.ui.data_source.currentIndex()) + 1

        conn = database_connect()
        cur = conn.cursor()
        try:
            if data_source == 4:
                sql = "SELECT * FROM tempurter WHERE main_time between %s and %s;"
                cur.execute(sql, (s_datetime_sql, e_datetime_sql))
                result = cur.fetchall()
                print(data_source)
            else:
                sql = "SELECT * FROM tempurter WHERE pot_num = %s and main_time between %s and %s;"
                cur.execute(sql, (data_source, s_datetime_sql, e_datetime_sql))
                result = cur.fetchall()
                print(data_source)

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
            # 设置表头信息，将mysql数据表中的表头信息拿出来，放进TableWidget中
            for i in col_result:
                item = QtWidgets.QTableWidgetItem()
                self.ui.sql_table_show.setHorizontalHeaderItem(a, item)
                item = self.ui.sql_table_show.horizontalHeaderItem(a)
                item.setText(self._translate("Form", i[0]))
                a = a + 1

            # 将数据格式改为列表形式，其是将数据库中取出的数据整体改为列表形式
            result = list(result)
            # 将相关的数据
            for i in range(len(result)):
                # 将获取的数据转为列表形式
                result[i] = list(result[i])
            for i in range(self.row):
                for j in range(self.vol):
                    self.Table_Data(i, j, result[i][j])

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
