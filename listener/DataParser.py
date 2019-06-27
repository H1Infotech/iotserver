import copy
import struct
class Parser(object):
    
    def __init__(self,ip,data):
        # 对于获取ASCII码的data 进行初步解析
        self.ip = ip
        if data:
            dataRes = data
            dataList = list()
            for i in range(0,len(dataRes),2):
                dataList.append(dataRes[i:i+2])
            self.data = dataList
            self.packetHeader = dataList[0] # 包头
            self.LHLW = dataList[1:2] # 长度高低
            self.deviceID = dataList[4:15] # 设备编号
            self.typeCode = dataList[16] # 类型码
            self.dataGroup = dataList[17] # 含有多少组信息 默认30组
            self.dataValue = dataList[18:] # 数值
        else:
            self.data = None
            self.packetHeader = None
            self.LHLW = None
            self.deviceID = None
            self.typeCode = None
            self.dataGroup = None
            self.dataValue = None

    def __byteTo(self,a,b):
        x = '{}{}ffff'.format(a,b)
        x = bytes.fromhex(x)
        res = struct.unpack('i',x)
        if not -300<res[0]/10<150:
            x = '{}{}0000'.format(a,b)
            x = bytes.fromhex(x)
            res = struct.unpack('i',x)
        return res[0]/10
    
    def __parser(self):

        data_ = list()
        data_g = list()
        result_ = list()
        result_g = list()
        # 把每一组信息数据解析成二维数组
        for i in self.dataValue:
                if str(i) != 'aa' and str(i) != 'bb':
                    data_.append(i)
                if str(i) == 'bb':
                    data_g.append(copy.deepcopy(data_))
                    data_.clear()
        # 遍历每组数值并且解析
        for i in data_g:
            year = int(i[1]+i[0],16) # 年
            month = int(i[2],16) #  月
            day = int(i[3],16) #  日
            hour = int(i[4],16) # 时 
            minute = int(i[5],16) # 分
            secound = int(i[6],16) # 秒
            deviceid = "".join(self.deviceID)
            result_=[ self.ip,int(self.dataGroup,16),int(deviceid,16),int(self.typeCode,16),year,month,day,hour,minute,secound]
            for k in range(0,len(i[7:23]),2):
                a = i[7:23][k]
                b = i[7:23][k+1]         
                result = self._Parser__byteTo(a,b)
                result_.append(result)
            result_.append(int(i[23],16))
            result_.append(int(i[24],16))
            result_.append(int(i[25],16))
            result_.append(int(i[26],16))
            result_.append(int(i[27],16))
            result_.append(int(i[28],16))
            result_.append(int(i[29],16))
            result_g.append(copy.deepcopy(result_))
            result_.clear()
        
        return result_g

    def __verification(self):
        x = list()
        for i in range(4,len(self.data)-2):
            x.append(int(self.data[i],16))
        if hex(sum(x))[-2:] == self.data[-2]:
            return True
        else:
            return False

    def run(self):
        if self._Parser__verification() == True:
            result = self.__parser()
            print("校验通过")
            return result
        else:
            print("校验失败")
            return None

