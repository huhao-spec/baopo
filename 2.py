# 浮点数
data = 123.41

def zhuanhaun(data):
    # 符号位
    nSign = 0x00 if data >= 0 else 0x01

    if data < 0:
        data = abs(data)

    nHead = int(data)
    fTail = data - nHead
    nHead = nHead << 1
    nHead = nHead >> 1
    str = ""
    for i in range(6):
        str += "0"
    str = bin(nHead)[2:].zfill(6)

    nHead_Length = len(str)

    nValue = nHead

    nShift = nHead_Length
    while nShift < 24:
        if (fTail * 2) >= 1:
            nValue = (nValue << 1) | 0x00000001
        else:
            nValue = (nValue << 1)
        temp = int(fTail * 2)
        fTail = (fTail * 2) - temp
        nShift += 1

    nExp = nHead_Length - 1 + 127
    nExp = nExp << 23
    nValue = nValue & 0x7FFFFF
    nValue = nValue | nExp
    nSign = nSign << 31
    nValue = nValue | nSign

    data1 = nValue & 0x000000FF
    data2 = (nValue & 0x0000FF00) >> 8
    data3 = (nValue & 0x00FF0000) >> 16
    data4 = (nValue >> 24) & 0x000000FF

    if data == 0:
        data1 = 0x00
        data2 = 0x00
        data3 = 0x00
        data4 = 0x00
    return data1,data2,data3,data4
number = zhuanhaun(data)
print(number)
# 将整数转换为一个包含各个位数的列表
# number_list = [int(digit) for digit in str(number)]
#
# print(number_list)
