# -*- coding: utf-8 -*-
import time

import cv2
from PyQt5.QtCore import QThread, pyqtSignal

from tools.predict import yuce


# 定义一个线程类
class jiance_Thread(QThread):
    # 自定义信号声明
    # 使用自定义信号和UI主线程通讯，参数是发送信号时附带参数的数据类型，可以是str、int、list等
    finishSignal = pyqtSignal(str)

    # 带一个参数t
    def __init__(self, ret, parent=None):
        super(jiance_Thread, self).__init__(parent)

        self.t = ret

    # run函数是子线程中的操作，线程启动后开始执行
    def run(self):
        self.c += 1
        if self.t:
            t1 = time.time()
            # 转换为RGB格式
            rgb_frame = cv2.cvtColor(self.t, cv2.COLOR_BGR2RGB)
            name = 'D:/BaiduNetdiskDownload/2/' + str(self.c) + '.jpg'
            cv2.imwrite(name, rgb_frame)
            print(self.text)
            if self.c % 8 == 0:
                # 调用深度学习检测界面
                yuce(name)
            t2 = time.time()
            print(t2 - t1)
