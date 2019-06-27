from postgres import Postgres

# id serial 自增主键
# ip IP地址
# data_contain 包含多少组数据
# year 年
# month 月
# day 日
# hour 时
# minute 分
# secound 秒
#  temp1 通道1
#  temp2 通道2
#  temp3 通道3
#  temp4 通道4
#  temp5 通道5
#  temp6 通道6
#  temp7 通道7
#  temp8 通道8
#  device_status 设备运行方式 1. 开机触发 2. 闹钟触发
#  collcetion_period 数据采集时间间隔
#  clock_status 时钟运行状态
# setting_status 配置状态 
# collect_error 通道错误
# battery 电池电压
# check 校验和


column = ['id','ip','data_contain','deviceid','typecode','year','month','day','hour','minute','secound','temp1','temp2','temp3','temp4','temp5','temp6','temp7','temp8','device_status','collcetion_period','clock_status','setting_status','collect_error','battery','checkr']
column_type = ['serial,','text,','text,','text,','integer,','integer,','integer,','integer,','integer,','integer,','integer,','float8,','float8,','float8,','float8,','float8,','float8,','float8,','float8,','integer,','float8,','integer,','integer,','integer,','float8,','text']
columnName = ('ip','data_contain','deviceid','typecode','year','month','day','hour','minute','secound','temp1','temp2','temp3','temp4','temp5','temp6','temp7','temp8','device_status','collcetion_period','clock_status','setting_status','collect_error','battery','checkr')
# 数据库连接器
class PSQL(object):
    
    def __init__(self, username, password, hostname, hostport, database):
        self.db = Postgres("postgres://{}:{}@{}:{}/{}".format(
                                                            username,
                                                            password,
                                                            hostname,
                                                            hostport,
                                                            database
                                                            ))

    def cursor(self,sql):
        self.db.run(sql)


def tableCreator(tablename):
    creater = "CREATE TABLE " + tablename + "( "
    tmp_f_creater = ""
    for i in range(len(column)):
        tmp_f_creater = tmp_f_creater + column[i] + " " + column_type[i]
    sql = str(creater+tmp_f_creater).rstrip(",")+")"
    return sql

def tableInsert(tablename,data):
    data = [tuple(i) for i in data]
    sql = "INSERT INTO " + tablename + str(columnName).replace("'", "")\
        + " VALUES "
    VALUES = ""
    for columns in data:
        TMP = ""
        TMP = "("+",".join("'"+str(row)+"'" for row in columns)+")"
        VALUES += TMP + ","
    sql = sql + VALUES.rstrip(",")
    return sql

