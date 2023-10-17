import datetime
import json
import sys
import time

import cv2
import pymysql
import pyqtgraph as pg
import torch
from PIL import Image
from torchvision import transforms

from login import *
from interfaceui import *
from interface import  *
from camera import *
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
from PyQt5.QtCore import QTimer
from model_mobile_net import efficientnet_b0 as create_model

#pip freeze > requirements.txt
user_now = ''#当前用户
cameras = ""#摄像头频道
crystal =  "" #结晶状态
temperature = ''#温度
account = ""#用户复写


def database_connect():
        connect = pymysql.connect(
                host = '127.0.0.1' 
                ,user = 'root' 
                ,passwd='123456'
                ,port= 3306
                ,db='main_data'
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
        
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)
        #----------------------------------------------------------------

        self.ui.textBrowser_1.append(cameras)

        #模拟
        # 创建 QLabel 控件用于显示图像
        self.image_label1_0 = QLabel()
        # 加载图像
        self.update_frame3()
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label1_0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label1_0.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小

        image_label1 = QLabel()
        pixmap = QPixmap("test.jpg")
        image_label1.setPixmap(pixmap)
        image_label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label1.setScaledContents(True)

        # 将 QLabel 控件添加到布局中
        self.ui.verticalLayout_camera.addWidget(self.image_label1_0)
        #------------------------------------------------------------------------------------

        self.ui.pushButton_return.clicked.connect(self.goreturn)
        #self.win = InterfaceWindow()
        self.win = Interfacepro()
        if account == '1':
            self.call_other_show()
        else:
            self.call_other_hide()
        self.show()
        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # create model
        self.model = create_model(num_classes=3).to(self.device)

        # load model weights
        model_weight_path = "D:/undergrate_project/rongyexijing/weights/0.997.pth"
        self.model.load_state_dict(torch.load(model_weight_path, map_location=self.device))
        self.model.eval()
    def call_other_hide(self):
        self.win.ui.pushButton_manage.hide()

    def call_other_show(self):
        self.win.ui.pushButton_manage.show()

    def init_plot(self):
        self.plotWidget = pg.PlotWidget()
        self.plotWidget.setTitle("实时数据折线图")
        self.plotWidget.setLabel("left", "数据值")
        self.plotWidget.setLabel("bottom", "时间","s")
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
        sql = "SELECT tem FROM tempurter ORDER BY id DESC LIMIT 1"
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
    def update_frame3(self):
        url = 'rtsp://admin:a12345678@192.168.2.3'
        # 调用定时器更摄像头
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        self.camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
        name = 'D:/BaiduNetdiskDownload/2/' + str(datetime.date.today()) + '.avi'
        self.out = cv2.VideoWriter(name, fourcc, 20, (640, 480))

        self.timer1 = QTimer(self)
        self.c_int = 0
        self.timer1.timeout.connect(self.update_img3)
        self.timer1.start()

    def update_img3(self):
        # 写入时间
        datetime = QtCore.QDateTime.currentDateTime()
        self.ui.textBrowser_4.clear()
        text = datetime.toString('HH:mm:ss')
        self.ui.textBrowser_4.append(text)

        # 写入温度
        # a = self.c.ReadData('VD', 56)  # 目标温度
        # self.ui.textBrowser_3.clear()
        # temperature = str(a)
        # print(temperature)
        # self.ui.textBrowser_3.append(temperature)

        # 摄像头更新实现函数
        ret, frame = self.camera.read()  # 读取摄像头帧

        frame = cv2.putText(frame, text, (200, 100), cv2.FONT_HERSHEY_COMPLEX, 2.0, (100, 200, 200), 5)
        self.out.write(frame)
        self.c_int += 1

        if ret:
            t1 = time.time()

            # 转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            # self.name = 'D:/BaiduNetdiskDownload/2/' + str(self.c_int) + '.jpg'
            # cv2.imwrite(self.name, frame)
            # cv2.putText(frame,str(self.c_int),(2000,2000),cv2.FONT_HERSHEY_PLAIN,10,(255,255,255),)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label1_0.setPixmap(pixmap)
            # if self.c_int % 8 == 0:
            # 调用深度学习检测界面

            with torch.no_grad():
                # img = Image.open(frame)
                img = Image.fromarray(frame.astype('uint8')).convert('RGB')
                data_transform = transforms.Compose(
                    [transforms.Resize(224),
                     transforms.CenterCrop(224),
                     transforms.ToTensor(),
                     transforms.Normalize([0.485, 0.456, 0.406], [0.229, 0.224, 0.225])])
                # [N, C, H, W]
                img = data_transform(img)
                # expand batch dimension
                img = torch.unsqueeze(img, dim=0)
                # read class_indict
                json_path = 'class_indices.json'
                with open(json_path, "r") as f:
                    class_indict = json.load(f)
                # predict class

                output = torch.squeeze(self.model(img.to(self.device))).cpu()
                predict = torch.softmax(output, dim=0)
                predict_cla = torch.argmax(predict).numpy()
            print_res = "class: {}".format(class_indict[str(predict_cla)])
            print(print_res)
            crystal_jieguo = print_res
            crystal_jieguo = str(crystal_jieguo)
            self.ui.textBrowser_2.clear()
            self.ui.textBrowser_2.append(crystal_jieguo)
            t2 = time.time()
            print(t2 - t1)

    def goreturn(self):
        self.win.hide()
        self.timer1.stop()
        self.win.show()
        self.close()
        cameras = ""
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
        #self.win = InterfaceWindow()
        self.win = Interfacepro()
        self.show()
        # 创建OtherClass实例对象

    def call_other_hide(self):
        self.win.ui.pushButton_manage.hide()

    def call_other_show(self):
        self.win.ui.pushButton_manage.show()

    def on_state_changed(self, state):
        if state == 2:  # Qt.Checked
            self.ui.lineEdit.setText(account)
    # 管理员登录
    def go_to_inter_manage(self):
        global account
        account = self.ui.lineEdit_4.text()
        password = self.ui.lineEdit_5.text()
        flag = self.admin_check(account, password)
        if flag:
            self.win.hide()
            self.win.show()
            self.call_other_show()
            self.close()
        else:
            QtWidgets.QMessageBox.warning(
                self, 'Error', 'Invalid username or password')
    # 普通用户登录
    def go_to_inter(self):
        global account
        account = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        flag = self.nomal_usr_check(account, password)
        if flag:
            self.win.hide()
            self.win.show()
            self.call_other_hide()
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

class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_vc.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_decode.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_manage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_find.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_delete.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))

        # 隐藏管理员按钮，管理员登录才可以，需要数据库，此处为模拟，需点击复写才可实现
        # if account !="123456":
        #     self.ui.pushButton_manage.hide()
        # else:
        #     self.ui.pushButton_manage.show()
        # 模拟------------------------------------------------------------------------------------------
        # 创建 QLabel 控件用于显示图像
        self.image_label2_0 = QLabel()
        # 加载图像
        self.update_frame()
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label2_0.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label2_0.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中

        image_label1 = QLabel()
        pixmap = QPixmap("test.jpg")
        image_label1.setPixmap(pixmap)
        image_label1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label1.setScaledContents(True)

        image_label2 = QLabel()
        pixmap = QPixmap("test.jpg")
        image_label2.setPixmap(pixmap)
        image_label2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        image_label2.setScaledContents(True)

        self.ui.horizontalLayout_v1.addWidget(self.image_label2_0)
        self.ui.horizontalLayout_v2.addWidget(image_label1)
        self.ui.horizontalLayout_v3.addWidget(image_label2)
        # -------------------------------------------------------------------------------------------

        self.ui.pushButton.clicked.connect(self.log_out)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_v1.clicked.connect(self.go_to_inter1)
        self.ui.pushButton_v2.clicked.connect(self.go_to_inter2)
        self.ui.pushButton_v3.clicked.connect(self.go_to_inter3)

        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)


    def register(self):
        username = self.ui.lineEdit_register.text()
        #检查两次密码是否相同
        if(self.ui.lineEdit_decode == self.ui.lineEdit_AffirmDecode):
            password = self.ui.lineEdit_decode
        else:
            QtWidgets.QMessageBox.warning(
                self, '错误', '两次密码输入不正确,请重新输入!')
            return False

        conn = database_connect()
        cur = conn.cursor()
        cur.execute("SELECT tem FROM tempurter ORDER BY id DESC LIMIT 1") 
        value = cur.fetchone()[0] 
        conn.close()
    
    def update_frame(self):
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        url = 'rtsp://admin:a12345678@169.254.18.238/h264/ch1/sub/av_stream'
        self.camera = cv2.VideoCapture(mp)
        self.timer1 = QTimer(self)
        self.timer1.timeout.connect(self.update_img)
        self.timer1.start()

    def update_img(self):
        ret, frame = self.camera.read()  # 读取摄像头帧
        if ret:
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)  # 转换为RGB格式
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label2_0.setPixmap(pixmap)
    def go_to_inter1(self):
        self.timer1.stop()
        self.close()
        global cameras
        cameras = "频道1"
        self.login = CameraWindow()
    def go_to_inter2(self):
        self.close()
        global cameras
        cameras = "频道2"
        self.login = CameraWindow()
    def go_to_inter3(self):
        self.close()
        global cameras
        cameras = "频道3"
        self.login = CameraWindow()

    def log_out(self):
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

class Interfacepro(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2pro()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_return1.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_return.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_ch_decode.clicked.connect(lambda:self.ui.stackedWidget.setCurrentIndex(1))
        self.ui.pushButton_manage.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(2))

        self.ui.pushButton_register.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(0))
        self.ui.pushButton_find.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(1))
        self.ui.pushButton_delete.clicked.connect(lambda: self.ui.stackedWidget_2.setCurrentIndex(2))

        # 隐藏管理员按钮，管理员登录才可以，需要数据库，此处为模拟，需点击复写才可实现
        # if account !="123456":
        #     self.ui.pushButton_manage.hide()
        # else:
        #     self.ui.pushButton_manage.show()
        # 模拟------------------------------------------------------------------------------------------
        # 创建 QLabel 控件用于显示图像
        # image_label = self.ui.label_v1
        # 加载图像
        pixmap = QPixmap("test.jpg")  # 替换为您实际的图像文件路径
        self.ui.label_v1.setPixmap(pixmap)
        # 设置 QLabel 的大小策略为 Expanding
        self.ui.label_v1.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v1.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中

        # image_label1 = QLabel()
        pixmap = QPixmap("test.jpg")
        self.ui.label_v2.setPixmap(pixmap)
        self.ui.label_v2.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.ui.label_v2.setScaledContents(True)

        # image_label2 = QLabel()
        pixmap = QPixmap("test.jpg")
        self.ui.label_v3.setPixmap(pixmap)
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

    def go_to_inter1(self):
        self.close()
        global cameras
        cameras = "频道1"
        self.login = CameraWindow()
    def go_to_inter2(self):
        self.close()
        global cameras
        cameras = "频道2"
        self.login = CameraWindow()
    def go_to_inter3(self):
        self.close()
        global cameras
        cameras = "频道3"
        self.login = CameraWindow()

    def log_out(self):
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



if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())