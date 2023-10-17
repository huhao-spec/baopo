from PyQt5.QtWidgets import QMainWindow, QPushButton, QApplication
import sys

# 其他类定义
class OtherClass:
    def other_method(self):
        print("调用了其他类的方法")

# 主窗口类
class MyMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.pushButton_wash = QPushButton(self)
        self.pushButton_wash.setText("Wash")
        self.pushButton_wash.clicked.connect(self.call_other_method)

        # 创建OtherClass实例对象
        self.other_object = OtherClass()

    def call_other_method(self):
        # 调用OtherClass的other_method方法
        self.other_object.other_method()

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MyMainWindow()
    window.show()
    sys.exit(app.exec_())