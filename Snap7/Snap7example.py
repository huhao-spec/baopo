# _*_ coding: utf-8 _*_

from Snap7.pySnap7 import Smart200

if __name__ == '__main__':
    # 连接PLC
    c = Smart200('192.168.2.10')
    ret = c.ConnectPLC()
    print(ret)
    while ret:

        """ I区读取 """
        a = c.ReadData('I', 0.0)
        print(a)
        a = c.ReadData('IB', 0)
        print(a)
        a = c.ReadData('IW', 0)
        print(a)
        a = c.ReadData('ID', 0)
        print(a)

        """ Q区读写 """
        a = c.WriteData('Q', 0.0, 1)
        print(a)
        a = c.ReadData('Q', 0.0)
        print(a)

        a = c.WriteData('QB', 0, 2)
        print(a)
        a = c.ReadData('QB', 0)
        print(a)

        a = c.WriteData('QW', 0, 258)
        print(a)
        a = c.ReadData('QW', 0)
        print(a)

        a = c.WriteData('QD', 0, 65538)
        print(a)
        a = c.ReadData('QD', 0)
        print(a)
        #
        """ M区读写 """
        a = c.WriteData('M', 0.0, 1)
        print(a)
        a = c.ReadData('M', 0.0)
        print(a)

        a = c.WriteData('MB', 0, 2)
        print(a)
        a = c.ReadData('MB', 0)
        print(a)

        a = c.WriteData('MW', 0, 258)
        print(a)
        a = c.ReadData('MW', 0)
        print(a)

        a = c.WriteData('MD', 0, 65538)
        print(a)
        a = c.ReadData('MD', 0)
        print(a)

        """ V区读写 """
        a = c.WriteData('V', 0.0, 1)
        print(a)
        a = c.ReadData('V', 0.0)
        print(a)

        a = c.WriteData('VB', 0, 2)
        print(a)
        a = c.ReadData('VB', 0)
        print(a)

        a = c.WriteData('VW', 0, 258)
        print(a)
        a = c.ReadData('VW', 0)
        print(a)

        a = c.WriteData('VD', 0, 65538)
        print(a)
        a = c.ReadData('VD', 0)
        print(a)

        # 判断错误代码
        e = a['statue']
        if e == -1:
            print('连接断开')
            c.CloseConnect()
            break
        elif e == 0:
            # 正常状态无错误
            pass
        else:
            print('地址错误')

        # 延时
        c.wait(2)
