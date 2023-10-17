import json

import numpy as np

from model_mobile_net import efficientnet_b0 as create_model
import cv2
import torch
import datetime
from PyQt5.QtCore import QTimer
from torchvision import transforms
from PIL import Image, ImageDraw, ImageFont
from login import *
from interfaceui import *
from camera import *
import sys
import time
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QMainWindow
from PyQt5.QtGui import QPixmap, QImage
from PyQt5.QtWidgets import QApplication, QLabel, QSizePolicy
from Snap7.pySnap7 import Smart200

#pip freeze > requirements.txt
user_now = ''#当前用户
cameras = ""#摄像头频道
crystal =  "" #结晶状态
account = ""#用户复写

class CameraWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow3()
        self.ui.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        self.ui.pushButton.clicked.connect(self.log_out)
        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)

        # 链接PLC
        # self.c = Smart200('192.168.2.1')
        # ret = self.c.ConnectPLC()
        # self.c.WriteData('V', 2.2, 1)
        # print(ret)
        #
        # a = self.c.ReadData('VD', 56)
        # print(a)

        #模拟

        temperature = '78.98'
        #----------------------------------------------------------------

        self.ui.textBrowser_1.append(cameras)

        #模拟
        # 创建 QLabel 控件用于显示图像
        self.image_label = QLabel()
        # 加载图像
        self.update_frame()
        # 设置 QLabel 的大小策略为 Expanding
        self.image_label.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.image_label.setScaledContents(True)  # 图片自动拉伸到 QLabel 大小
        # 将 QLabel 控件添加到布局中
        self.ui.horizontalLayout_timevc.addWidget(self.image_label)
        #------------------------------------------------------------------------------------

        self.ui.pushButton_return.clicked.connect(self.goreturn)

        self.show()

        self.device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

        # create model
        self.model = create_model(num_classes=3).to(self.device)

        # load model weights
        model_weight_path = "D:/undergrate_project/rongyexijing/weights/0.997.pth"
        self.model.load_state_dict(torch.load(model_weight_path, map_location=self.device))
        self.model.eval()

    def update_frame(self):
        url = 'rtsp://admin:a12345678@192.168.2.3'
        # 调用定时器更摄像头
        mp = 'D:/BaiduNetdiskDownload/new_video.mp4'
        self.camera = cv2.VideoCapture(0)
        fourcc = cv2.VideoWriter.fourcc('m', 'p', '4', 'v')
        name = 'D:/BaiduNetdiskDownload/2/'+str(datetime.date.today())+'.avi'
        self.out = cv2.VideoWriter(name, fourcc, 20, (640, 480))

        self.timer1 = QTimer(self)
        self.c_int = 0
        self.timer1.timeout.connect(self.update_img)
        self.timer1.start()

    def update_img(self):
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
            self.image_label.setPixmap(pixmap)
            if self.c_int % 8 == 0:
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
            print(t2-t1)

    def cv2AddChineseText(frame, text, position, textColor=(0, 255, 0), textSize=300):
        img_plg = Image.fromarray(frame)
        draw = ImageDraw.Draw(img_plg)
        # 字体的格式
        fontStyle = ImageFont.truetype(
            "./../font/simsun.ttc", textSize, encoding="utf-8")
        # 绘制文本
        img_array = draw.text(position, text, textColor, font=fontStyle)
        img = np.asarray(img_array)
        return img
    def goreturn(self):
        self.win = InterfaceWindow()
        self.timer1.stop()
        self.win.hide()
        self.win.show()
        self.close()
        self.camera.release()
        self.out.release()

        # 关闭PLC
        # self.c.WriteData('V', 2.2, 0)
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


        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
        self.setAttribute(QtCore.Qt.WA_TranslucentBackground)
        # 连接按钮的 clicked 信号
        self.ui.pushButton_3.clicked.connect(self.go_to_inter)
        # 连接复选框的状态变化信号到槽函数
        self.ui.checkBox.stateChanged.connect(self.on_state_changed)
        self.win = InterfaceWindow()
        self.show()

    def on_state_changed(self, state):
        if state == 2:  # Qt.Checked
            self.ui.lineEdit.setText(account)

    def go_to_inter(self):
        global account
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


class InterfaceWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow2()
        self.ui.setupUi(self)
        # self.setWindowFlags(QtCore.Qt.FramelessWindowHint)
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
        self.image_label = QLabel()
        # 加载图像
        self.update_frame()
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

        self.ui.pushButton_3.clicked.connect(self.toggle_fullscreen)

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
            self.image_label.setPixmap(pixmap)

    def go_to_inter1(self):
        self.timer1.stop()
        self.close()
        global cameras
        cameras = "频道1"
        self.login = CameraWindow()

        # 启动plc
        # self.c.WriteData('V', 2.2, 1)

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