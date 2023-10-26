# _*_ coding: utf-8 _*_

from Snap7.pySnap7 import Smart200

if __name__ == '__main__':
    # 连接PLC
    c = Smart200('192.168.2.1')
    ret = c.ConnectPLC()
    print(ret)
    if ret:
        A = c.WriteData('V', 8.0, 1)
        B = c.WriteData('V', 2.2, 1)
        d = c.WriteData('V', 5.3, 1)
        # 结晶信号：v5.3写1就是开始结晶
        e = c.ReadData('V', 5.3)
        a = c.ReadData('V', 8.0)
        b = c.ReadData('V', 2.2)
        print(a, b,'e',e)