import cv2
from PyQt5.QtWidgets import QMainWindow


class CameraSingleton:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance.camera = cv2.VideoCapture(0)
        return cls._instance


# 第一个界面
class FirstWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera = CameraSingleton().camera
        # ...


# 第二个界面
class SecondWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.camera = CameraSingleton().camera
        # ...


# 在你的主程序中
if __name__ == "__main__":
    app = QApplication(sys.argv)
    window1 = FirstWindow()
    window2 = SecondWindow()
    # 显示第一个界面，关闭后显示第二个界面
    window1.show()
    app.exec_()
    CameraSingleton().camera.release()  # 释放摄像头资源
