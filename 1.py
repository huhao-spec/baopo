from Snap7.pySnap7 import Smart200


def read_f(data1, data2, data3, data4):
    # 读数
    data1 = c.ReadData('VB', data1)
    data2 = c.ReadData('VB', data2)
    data3 = c.ReadData('VB', data3)
    data4 = c.ReadData('VB', data4)
    # 取数
    data1 = data1['data']
    data2 = data2['data']
    data3 = data3['data']
    data4 = data4['data']
    # 变类型
    data1 = int(''.join(map(str, data1)))
    data2 = int(''.join(map(str, data2)))
    data3 = int(''.join(map(str, data3)))
    data4 = int(''.join(map(str, data4)))
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
    return value


c = Smart200('192.168.2.1')
c.ConnectPLC()
# A=c.WriteData('VB', 7.0, 3) # 自动和远程合并 写0所有的都停 软件开始时候写入
B=c.WriteData('VB', 8, 1)   # 8代表视频开始结晶  视频识别到结晶时候写入
# a=c.ReadData('VB', 7)
b=c.ReadData('VB', 8)
print( b)
# print(read_f(900,901,902,903))
