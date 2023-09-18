import sys
import time

import cv2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
from PyQt5.QtWidgets import QMainWindow

from Snap7.pySnap7 import Smart200
from camera import *
from interfaceui import *
from login import *
from tools.predict import yuce

user_now = ''  # 当前用户
cameras = ""  # 摄像头频道
crystal = ""  # 结晶状态
temperature = ''  # 温度
ce = Smart200('192.168.2.1')
ret = ce.ConnectPLC()


# 析晶溶液检测界面
class CameraWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.log_out)
        # 模拟输入
        # 创建1个 QTimer计时器对象
        timer = QtCore.QTimer(self)
        # 发射timeout信号，与自定义槽函数关联
        timer.timeout.connect(self.showtime)
        # 启动计时器
        timer.start()

        # 实现对predict的返回值做出判断
        # 模拟
        crystal = "大量析晶"
        temperature = '78.98'
        # ----------------------------------------------------------------
        # 检测界面一些文本消息
        self.ui.textBrowser_1.append(cameras)
        self.ui.textBrowser_2.append(crystal)
        self.ui.textBrowser_3.append(temperature)

        # 创建 QLabel 控件用于显示图像
        self.image_label = QLabel()
        # 加载图像
        self.update_frame()
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中
        self.ui.horizontalLayout_timevc.addWidget(self.image_label)
        # ------------------------------------------------------------------------------------
        # 返回主界面按钮
        self.ui.pushButton_return.clicked.connect(self.goreturn)
        self.show()

    def update_frame(self):
        a = ce.WriteData('V', 2.2, 1)
        print(a)
        # 调用定时器更摄像头
        self.camera = cv2.VideoCapture(0)
        self.timer1 = QTimer(self)
        self.c = 0
        self.timer1.timeout.connect(self.update_img)
        self.timer1.start()

    def update_img(self):
        # 摄像头更新实现函数
        ret, frame = self.camera.read()  # 读取摄像头帧
        a = ce.ReadData('VD', 56)
        print(a)
        self.c += 1
        if ret:
            t1 = time.time()
            # 转换为RGB格式
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            name = 'D:/BaiduNetdiskDownload/2/' + str(self.c) + '.jpg'
            cv2.imwrite(name, rgb_frame)
            h, w, ch = rgb_frame.shape
            bytes_per_line = ch * w
            q_image = QImage(rgb_frame.data, w, h, bytes_per_line, QImage.Format_RGB888)
            pixmap = QPixmap.fromImage(q_image)
            self.image_label.setPixmap(pixmap)
            print(self.text)
            if self.c % 8 == 0:
                # 调用深度学习检测界面
                yuce(name)
            t2 = time.time()
            print(t2 - t1)

    # 自定义槽函数，用来在状态栏中显示当前日期时间
    def showtime(self):
        # 时间展示函数
        # 获取当前日期时间
        datetime = QtCore.QDateTime.currentDateTime()
        self.ui.textBrowser_4.clear()
        # 格式化日期时间
        self.text = datetime.toString('HH:mm:ss')
        self.ui.textBrowser_4.append(self.text)

    def goreturn(self):
        self.win = InterfaceWindow()
        self.timer1.stop()
        self.win.hide()
        self.win.show()
        self.close()
        cameras = ""

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


# 登录页面
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
        self.win = InterfaceWindow()
        self.show()

    def go_to_inter(self):
        account = self.ui.lineEdit.text()
        password = self.ui.lineEdit_2.text()
        if account == '1' and password == "1":
            self.win.hide()
            self.win.show()
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


# 登录后界面
class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton_vc.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(0))
        self.ui.pushButton_decode.clicked.connect(lambda: self.ui.stackedWidget.setCurrentIndex(1))

        # 模拟------------------------------------------------------------------------------------------
        # 创建 QLabel 控件用于显示图像
        self.image_label = QLabel()
        # 加载图像
        self.update_frame()
        # 替换为您实际的图像文件路径
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
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

        self.ui.horizontalLayout_v1.addWidget(self.image_label)
        self.ui.horizontalLayout_v2.addWidget(image_label1)
        self.ui.horizontalLayout_v3.addWidget(image_label2)
        # -------------------------------------------------------------------------------------------

        self.ui.pushButton.clicked.connect(self.log_out)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_v1.clicked.connect(self.go_to_inter1)
        self.ui.pushButton_v2.clicked.connect(self.go_to_inter2)
        self.ui.pushButton_v3.clicked.connect(self.go_to_inter3)

    def update_frame(self):
        self.camera = cv2.VideoCapture(0)
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
            self.image_label.setPixmap(pixmap)

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


if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = LoginWindow()
    sys.exit(app.exec_())
