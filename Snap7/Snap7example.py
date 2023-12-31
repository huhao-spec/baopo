# _*_ coding: utf-8 _*_

from Snap7.pySnap7 import Smart200

if __name__ == '__main__':
    # 连接PLC
    c = Smart200('192.168.2.1')
    ret = c.ConnectPLC()
    print(ret)
    if ret:
        # A = c.WriteData('V', 8.0, 1)
        # B = c.WriteData('V', 2.2, 1)
        # d = c.WriteData('V', 5.3, 1)
        # # 结晶信号：v5.3写1就是开始结晶
        # e = c.ReadData('V', 5.3)
        # a = c.ReadData('V', 8.0)
        # b = c.ReadData('V', 2.2)
        # o = c.ReadData('Q',0.1)
        # print(a, b,'e',e,'q0.1',o)
        # c.WriteData('VD', 600, 123.214)
        # print()
        """
        I区读取
        写入...........................................................................................................................................................................................................
        """
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

        """ V区读写
        输入V2.2开始输入，控制开始
        如果把设备输入
        a = c.WriteData('V', 2.2, 1)开始
        a = c.WriteData('V', 2.2, 0)关闭
        读取操作

        """
        a = c.WriteData('V', 0.0, 1)
        print(a)
        a = c.ReadData('V', 0.0)
        # a = c.ReadData('V', 0.5)读结晶信号。
        # a = c.ReadData('V', 5.1)视窗与罐内温度相差大。
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
        #  a = c.ReadData('VD', 48)读密度，都是浮点
        #  a = c.ReadData('VD', 44)读ph值接受浮点型数据
        #  a = c.ReadData('VD', 52)窗外温度
        #  a = c.ReadData('VD', 56)目标温度
        # 接近结晶信号：a = c.ReadData('I', 0.1)
        # 变频器运行信号：a = c.ReadData('I', 0.4)
        # 变频器故障信号：a = c.ReadData('I', 0.6)
        # 电磁阀吸合信号：a = c.ReadData('I', 0.7)
        # 照明信号：a = c.ReadData('I', 0.5)
        # c.WriteData('v',0.1, 1)
        # c.WriteData('v',2.2, 1) 自动控制两个都是1的时候自动运行

        print(a)
        A = c.WriteData('VB', 8.0, 1)
        B = c.WriteData('VB', 2.2, 1)
        d = c.WriteData('V', 5.3, 1)
        e = c.ReadData('V', 5.3)
        a = c.ReadData('V', 8.0)
        b = c.ReadData('V', 2.2)
        print("v8.0",a,"e", b,'e',e)
        c.WriteData('VD', 600, 123.214)
        print()

        # 判断错误代码
        e = a['statue']
        if e == -1:
            print('连接断开')
            c.CloseConnect()
        elif e == 0:
            # 正常状态无错误
            pass
        else:
            print('地址错误')

        # 延时
        c.wait(2)
