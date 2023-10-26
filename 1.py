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
    value = str(value)
    return value


c = Smart200('192.168.2.1')
c.ConnectPLC()

# 传入温度
tem = read_f(56, 57, 58, 59)
print(tem)

