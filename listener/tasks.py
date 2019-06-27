import os
import sys
curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)
from listener.insert import PSQL,tableCreator,tableInsert
from listener.DataParser import Parser
import redis
import json
#多任务队列
import datetime
from celery import Celery
import copy
from collections import defaultdict
CELERY_RESULT_BACKEND = 'redis://:123qweasdzxc@47.100.247.139:5432/2'
BROKER_URL  = 'redis://:123qweasdzxc@47.100.247.139:5432/3'
app = Celery('tasks', broker=BROKER_URL,backend=CELERY_RESULT_BACKEND)

#设定数据库连接配置 本地数据库
psql = PSQL('postgres','postgres','47.100.247.139','8660','platform')
pool = redis.ConnectionPool(host='47.100.247.139',port=5432, db=0,password='123qweasdzxc')
r = redis.Redis(connection_pool=pool)

#datalist
def list_to_json(datalist):
    """ datalist = [[],[],[]] """
    if datalist:

        dictmp = {}
        dictAll = {}
        dictAll['deviceInfo']={"voltage":datalist[0][23]}
        for i in range(len(datalist)):
        
            dictmp["ip"] = datalist[i][0]
            dictmp["groupNum"] = datalist[i][1]
            dictmp["DeviceID"] = datalist[i][2]
            time = str(datalist[i][4]) + "-" + str(datalist[i][5])+ "-" + str(datalist[i][6]) +" "+str(datalist[i][7])+":"+str(datalist[i][8])+":"+str(datalist[i][9])
            dictmp["datetime"] = time
            dictmp["tmp1"] = datalist[i][10]
            dictmp["tmp2"] = datalist[i][11]
            dictmp["tmp3"] = datalist[i][12]
            dictmp["tmp4"] = datalist[i][13]
            dictmp["tmp5"] = datalist[i][14]
            dictmp["tmp6"] = datalist[i][15]
            dictmp["tmp7"] = datalist[i][16]
            dictmp["tmp8"] = datalist[i][17]
            dictAll[str(i)] = copy.deepcopy(dictmp)
            dictmp.clear()
        
        res = json.dumps(dictAll)
        return dictAll["0"]["DeviceID"],res
    else:
        return "None",json.dumps({"error":"No data cache"})


@app.task(name="celery_queue")
def celery_queue(clientAddress, message):
    try:
        sql  = tableCreator("device_info_test")
        print(sql)
        psql.cursor(tableCreator("device_info_test"))
    except Exception as e:
        print(e)
        pass
    co = Parser(clientAddress[0],message)
    data = co.run()
    if data:
        sql = tableInsert("device_info_test",data)
        psql.cursor(sql)
        deviceID,res = list_to_json(data)
        r.set(deviceID,res)



# a = b'h\xce\x03h\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\xff\x08\x1e\xaa\xe3\x07\x03\x1d\x0b\'\x00\xc9\x00\xc9\x00\x18\xf5\x1b\xf5\xd3\x00\x1a\xf5\xca\x00\x19\xf5\x01\n\x00\x00"\xac\xd2\xbb\xaa\xe3\x07\x03\x1d\x0b1\x00\xdf\x00\xca\x00\x18\xf5\x1a\xf5\xcd\x00\x1a\xf5\xcd\x00\x18\xf5\x02\n\x00\x00#\xac\xf0\xbb\xaa\xe3\x07\x03\x1d\x0b4\x00\xe0\x00\xca\x00\x18\xf5\x19\xf5\xcc\x00\x19\xf5\xce\x00\x18\xf5\x02\n\x00\x00#\xac\xf2\xbb\xaa\xe3\x07\x03\x1d\x0b9\x00\xf6\x00\xcc\x00\x17\xf5\x1b\xf5\xdb\x00\x1a\xf5\xda\x00\x19\xf5\x01\n\x00\x00#\xac,\xbb\xaa\xe3\x07\x03\x1d\x0b;\x00\xf4\x00\xcd\x00\x18\xf5\x1c\xf5\xe3\x00\x19\xf5\xde\x00\x19\xf5\x01\n\x00\x00#\xac:\xbb\xaa\xe3\x07\x03\x1d\x0c\t\x00\xd2\x00\xc9\x00\x17\xf5\x19\xf5\xd8\x00\x19\xf5\xe3\x00\x17\xf5\x02\n\x00\x00#\xac\xd8\xbb\xaa\xe3\x07\x03\x1d\x0c\x13\x00\xce\x00\xc7\x00\x17\xf5\x1a\xf5\xc9\x00\x19\xf5\xea\x00\x18\xf5\x02\n\x00\x00#\xac\xd6\xbb\xaa\xe3\x07\x03\x1d\x0c\x1d\x00\xcb\x00\xc7\x00\x17\xf5\x1a\xf5\xc7\x00\x19\xf5\xec\x00\x17\xf5\x02\n\x00\x00#\xac\xdc\xbb\xaa\xe3\x07\x03\x1d\x0c\'\x00\xcb\x00\xc7\x00\x17\xf5\x19\xf5\xc6\x00\x19\xf5\xeb\x00\x17\xf5\x02\n\x00\x00#\xac\xe3\xbb\xaa\xe3\x07\x03\x1d\x0c1\x00\xca\x00\xc7\x00\x17\xf5\x19\xf5\xc6\x00\x19\xf5\xe9\x00\x17\xf5\x02\n\x00\x00$\xac\xeb\xbb\xaa\xe3\x07\x03\x1d\x0c3\x00\xc9\x00\xc6\x00\x17\xf5\x19\xf5\xc5\x00\x19\xf5\xe7\x00\x17\xf5\x02\n\x00\x00$\xac\xe8\xbb\xaa\xe3\x07\x03\x1d\x0c;\x00\xcb\x00\xc8\x00\x18\xf5\x19\xf5\xca\x00\x19\xf5\xd6\x00\x18\xf5\x02\n\x00\x00$\xac\xea\xbb\xaa\xe3\x07\x03\x1d\r\t\x00\xca\x00\xca\x00\x18\xf5\x19\xf5\xca\x00\x19\xf5\xd1\x00\x18\xf5\x02\n\x00\x00$\xac\xb5\xbb\xaa\xe3\x07\x03\x1d\r\x13\x00\xd2\x00\xcc\x00\x17\xf5\x19\xf5\xe1\x00\x1a\xf5\xd6\x00\x17\xf5\x02\n\x00\x00$\xac\xe4\xbb\xaa\xe3\x07\x03\x1d\r\x1d\x00\xcf\x00\xd0\x00\x17\xf5\x19\xf5\xcd\x00\x19\xf5\xde\x00\x18\xf5\x02\n\x00\x00$\xac\xe3\xbb\xaa\xe3\x07\x03\x1d\r\'\x00\xd5\x00\xd0\x00\x18\xf5\x1a\xf5\xd4\x00\x19\xf5\xdd\x00\x17\xf5\x02\n\x00\x00$\xac\xfa\xbb\xaa\xe3\x07\x03\x1d\r1\x00\xd2\x00\xcf\x00\x16\xf5\x19\xf5\xd0\x00\x19\xf5\xd1\x00\x17\xf5\x02\n\x00\x00%\xac\xee\xbb\xaa\xe3\x07\x03\x1d\r;\x00\xd1\x00\xcd\x00\x17\xf5\x19\xf5\xcb\x00\x19\xf5\xd4\x00\x17\xf5\x02\n\x00\x00%\xac\xf4\xbb\xaa\xe3\x07\x03\x1d\x0e\t\x00\xd0\x00\xcd\x00\x17\xf5\x19\xf5\xc9\x00\x19\xf5\xd0\x00\x17\xf5\x02\n\x00\x00%\xac\xbc\xbb\xaa\xe3\x07\x03\x1d\x0e\x13\x00\xd4\x00\xce\x00\x17\xf5\x19\xf5\xca\x00\x19\xf5\xd6\x00\x17\xf5\x02\n\x00\x00%\xac\xd2\xbb\xaa\xe3\x07\x03\x1d\x0e\x1d\x00\xd3\x00\xcc\x00\x17\xf5\x19\xf5\xcb\x00\x19\xf5\xd5\x00\x17\xf5\x02\n\x00\x00%\xac\xd9\xbb\xaa\xe3\x07\x03\x1d\x0e\'\x00\xd5\x00\xca\x00\x16\xf5\x19\xf5\xcd\x00\x19\xf5\xd5\x00\x17\xf5\x02\n\x00\x00%\xac\xe4\xbb\xaa\xe3\x07\x03\x1d\x0e1\x00\xd2\x00\xd1\x00\x17\xf5\x19\xf5\xce\x00\x19\xf5\xd5\x00\x17\xf5\x02\n\x00\x00&\xac\xf5\xbb\xaa\xe3\x07\x03\x1d\x0e;\x00\xd4\x00\xd2\x00\x17\xf5\x1b\xf5\xd0\x00\x19\xf5\xd5\x00\x18\xf5\x01\n\x00\x00&\xac\x06\xbb\xaa\xe3\x07\x03\x1d\x0f\t\x00\xdd\x00\xd5\x00\x17\xf5\x19\xf5\xe8\x00\x19\xf5\xce\x00\x17\xf5\x02\n\x00\x00&\xac\xf0\xbb\xaa\xe3\x07\x03\x1d\x0f\x13\x00\xde\x00\xd3\x00\x17\xf5\x19\xf5\xea\x00\x1a\xf5\xce\x00\x17\xf5\x02\n\x00\x00&\xac\xfc\xbb\xaa\xe3\x07\x03\x1d\x0f\x1d\x00\xca\x00\xd7\x00\x17\xf5\x19\xf5\xc8\x00\x19\xf5\xcb\x00\x17\xf5\x02\n\x00\x00\'\xac\xd1\xbb\xaa\xe3\x07\x03\x1d\x0f&\x00\xc8\x00\xd7\x00\x17\xf5\x19\xf5\xc5\x00\x19\xf5\xc8\x00\x17\xf5\x02\n\x00\x00\'\xac\xd2\xbb\xaa\xe3\x07\x03\x1d\x0f0\x00\xc7\x00\xd5\x00\x17\xf5\x19\xf5\xc6\x00\x19\xf5\xc8\x00\x17\xf5\x02\n\x00\x00\'\xac\xda\xbb\xaa\xe3\x07\x03\x1d\x0f:\x00\xc7\x00\xd4\x00\x17\xf5\x19\xf5\xc6\x00\x19\xf5\xc8\x00\x18\xf5\x02\n\x00\x00\'\xac\xe4\xbbv\x16'
# co = Parser("117.132.191.90",a.hex())
# data = co.run()
# deviceID,res = list_to_json(data)
# r.set(deviceID,res)
# print(r.get(deviceID))
#309485009821345068724781055,