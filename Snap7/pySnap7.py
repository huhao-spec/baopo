# _*_ coding: utf-8 _*_
import struct
import time

import snap7
from snap7 import util

""" Debug 装饰器 """


def Debug(func):
    # 调试装饰器
    def Function(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except Exception as e:
            print(e)
            result = None
        return result

    return Function


class Smart200():

    def __init__(self, ip: str):
        ""
        """
        read_area(area, dbnumber, start, size)
        这是读plc最重要的方法，功能强大，支持（I，Q，M，DB，V，CT，TM）多存储区读取数据
        area：区地址类型（十六进制类型），如下图对应
        dbnumber：地址编号（int），只适用于DB区和200samart的V区，其它区全默认0，V区只能填1
        start：要读取数据的字节起始地址（int）
        size：要读取的数据类型所占字节长度大小（int）
        """
        self.__ip = ip

        self.__isConnect = False
        self.__dataArray = ['I', 'IB', 'IW', 'ID',
                            'Q', 'QB', 'QW', 'QD',
                            'M', 'MB', 'MW', 'MD',
                            'V', 'VB', 'VW', 'VD', ]

        self.__ClientAreas = {'I': snap7.client.Areas.PE,
                              'Q': snap7.client.Areas.PA,
                              'M': snap7.client.Areas.MK,
                              'V': snap7.client.Areas.DB, }

    def ConnectPLC(self):
        try:
            # 创建通讯客户端实例
            self.__plc = snap7.client.Client()
            # 连接至PLC
            self.__plc.connect(self.__ip, 0, 1)
            # 获取连接状态
            self.__isConnect = self.__plc.get_connected()
            print('connect successful')
            return True
        except:
            self.__isConnect = False
            return False

    @Debug
    def CloseConnect(self):
        if self.__plc != None:
            self.__plc.disconnect()
            self.__plc.destroy()
            self.__plc, self.__isConnect = None, False
        else:
            pass

    def ReadData(self, _array: str, _index: float):

        returnParams = dict()

        if not self.__isConnect:
            returnParams['statue'] = self.__Error(False)
            returnParams['data'] = []
        else:
            try:
                # 变为大写
                _array = _array.upper()
                # 判断V区
                if 'V' in _array:
                    dbNum = 1
                else:
                    dbNum = 0
                # 判断模式
                if 'I' in _array:
                    clientArea = self.__ClientAreas['I']
                elif 'Q' in _array:
                    clientArea = self.__ClientAreas['Q']
                elif 'M' in _array:
                    clientArea = self.__ClientAreas['M']
                elif 'V' in _array:
                    clientArea = self.__ClientAreas['V']
                else:
                    returnParams['statue'] = self.__Error(False)
                    returnParams['data'] = []
                    return returnParams

                # 解析地址
                _index = [int(i) for i in str(_index).split('.')]
                # 寻找对应函数
                if _array == 'I' or _array == 'Q' or _array == 'M' or _array == 'V':
                    f = self.__coils(clientArea, _index[0], _index[1], 0, dbNum)
                    returnParams['statue'] = self.__Error(True)
                    returnParams['data'] = f['data']
                elif 'B' in _array:
                    f = self.__registersB(clientArea, _index[0], 0, dbNum)
                    returnParams['statue'] = self.__Error(True)
                    returnParams['data'] = f['data']
                elif 'W' in _array:
                    f = self.__registersW(clientArea, _index[0], 0, dbNum)
                    returnParams['statue'] = self.__Error(True)
                    returnParams['data'] = f['data']
                elif 'D' in _array:
                    f = self.__registersD(clientArea, _index[0], 0, dbNum)
                    returnParams['statue'] = self.__Error(True)
                    returnParams['data'] = f['data']
                else:
                    returnParams['statue'] = self.__Error(False)
                    returnParams['data'] = []
                    return returnParams

            except Exception as e:
                if type(e) == RuntimeError:
                    self.__isConnect = False
                    returnParams['statue'] = self.__Error(False)
                    returnParams['data'] = []
                else:
                    self.__isConnect = True
                    returnParams['statue'] = self.__Error(False)
                    returnParams['data'] = []

        return returnParams

    def WriteData(self, _array: str, _index: float, _data: int):
        returnParams = dict()

        if not self.__isConnect:
            returnParams['statue'] = self.__Error(False)
            returnParams['data'] = []

        else:
            try:
                # 变为大写
                _array = _array.upper()
                # 判断V区
                if 'V' in _array:
                    dbNum = 1
                else:
                    dbNum = 0
                # 判断模式
                if 'Q' in _array:
                    clientArea = self.__ClientAreas['Q']
                elif 'M' in _array:
                    clientArea = self.__ClientAreas['M']
                elif 'V' in _array:
                    clientArea = self.__ClientAreas['V']
                else:
                    returnParams['statue'] = self.__Error(False)
                    return returnParams

                # 解析地址
                _index = [int(i) for i in str(_index).split('.')]
                # 寻找对应函数
                if _array == 'Q' or _array == 'M' or _array == 'V':
                    self.__coils(clientArea, _index[0], _index[1], 1, dbNum, _data)
                    returnParams['statue'] = self.__Error(True)
                elif 'B' in _array:
                    self.__registersB(clientArea, _index[0], 1, dbNum, _data)
                    returnParams['statue'] = self.__Error(True)
                elif 'W' in _array:
                    self.__registersW(clientArea, _index[0], 1, dbNum, _data)
                    returnParams['statue'] = self.__Error(True)
                elif 'D' in _array:
                    self.__registersD(clientArea, _index[0], 1, dbNum, _data)
                    returnParams['statue'] = self.__Error(True)
                else:
                    returnParams['statue'] = self.__Error(False)
                    return returnParams


            except Exception as e:
                if type(e) == RuntimeError:
                    self.__isConnect = False
                    returnParams['statue'] = self.__Error(False)
                else:
                    self.__isConnect = True
                    returnParams['statue'] = self.__Error(False)

        return returnParams

    @Debug
    def wait(self, second: float):
        time.sleep(second)

    def __Error(self, statue):
        if not self.__isConnect:
            return -1  # 连接失败
        else:
            if statue:
                return 0  # 无错误
            else:
                return 1  # 读取或者写入失败

    def __coils(self, _clientArea, _index1, _index2, _mode, _dbNum, *args):

        returnParams = dict()
        # 根据地址读取数据
        data = self.__plc.read_area(_clientArea, _dbNum, _index1, 1)
        if _mode == 0:  # 读取模式
            # 解析数据
            returnParams['data'] = [1 if util.get_bool(data, 0, _index2) else 0]

        else:  # 写入模式
            # 变为二进制数据
            _ = self.__DecToBin(struct.unpack('B', data)[0])[::-1]
            # 更改数据
            _[_index2] = args[0]
            # 组成发送数据
            _send = struct.pack('B', sum([_[i] * (2 ** i) for i in range(0, 8)]))
            self.__plc.write_area(_clientArea, _dbNum, _index2, bytearray(_send))

        return returnParams

    def __registersB(self, _clientArea, _index, _mode, _dbNum, *args):
        returnParams = dict()
        if _mode == 0:
            # 根据地址读取数据
            data = self.__plc.read_area(_clientArea, _dbNum, _index, 1)
            # 解析数据
            returnParams['data'] = list(struct.unpack('B' * len(data), data))
        else:
            _send = struct.pack('B', args[0])
            self.__plc.write_area(_clientArea, _dbNum, _index, bytearray(_send))

        return returnParams

    def __registersW(self, _clientArea, _index, _mode, _dbNum, *args):
        returnParams = dict()

        if _mode == 0:
            # 根据地址读取数据
            data = self.__plc.read_area(_clientArea, _dbNum, _index, 2)
            # 解析数据
            _ = list(struct.unpack('B' * len(data), data))
            returnParams['data'] = [_[0] * 256 + _[1]]
        else:
            _send = struct.pack('>H', args[0])
            self.__plc.write_area(_clientArea, _dbNum, _index, bytearray(_send))

        return returnParams

    def __registersD(self, _clientArea, _index, _mode, _dbNum, *args):
        returnParams = dict()
        if _mode == 0:
            # # 根据地址读取数据
            data = self.__plc.read_area(_clientArea, _dbNum, _index, 4)
            # 解析数据
            _ = list(struct.unpack('B' * len(data), data))
            returnParams['data'] = [(_[0] * 256 + _[1]) * 65536 + (_[0] * 256 + _[1])]

        else:
            _send = struct.pack('>H', int(args[0] / 65536)) + struct.pack('>H', int(args[0] % 65536))
            self.__plc.write_area(_clientArea, _dbNum, _index, bytearray(_send))

        return returnParams

    def __DecToBin(self, data: int, length=8):
        ""
        """
        十进制转二进制
        :param data: 
        :return: 
        """
        _ = [int(i) for i in bin(data).replace('0b', '')]
        return [0] * (length - len(_)) + _
