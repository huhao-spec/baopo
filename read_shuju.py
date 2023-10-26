from Snap7.pySnap7 import Smart200


def read_f(self, data1_int, data2_int, data3_int, data4_int):
    # 读数
    plc_read = Smart200('192.168.2.1')
    plc_read.ConnectPLC()
    data1_ori = plc_read.ReadData('VB', data1_int)
    data2_ori = plc_read.ReadData('VB', data2_int)
    data3_ori = plc_read.ReadData('VB', data3_int)
    data4_ori = plc_read.ReadData('VB', data4_int)
    # print(data1_ori)       # 取数
    data1_data = data1_ori['data']
    data2_data = data2_ori['data']
    data3_data = data3_ori['data']
    data4_data = data4_ori['data']
    # 变类型
    data1 = int(''.join(map(str, data1_data)))
    data2 = int(''.join(map(str, data2_data)))
    data3 = int(''.join(map(str, data3_data)))
    data4 = int(''.join(map(str, data4_data)))
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