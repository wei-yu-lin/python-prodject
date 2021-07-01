from os import write
import pyodbc
import pandas as pd
import json
import time
import cx_Oracle
import math
import re



def checkRdbTable(ps, db):
    with open('account.json', 'r') as data_file:
        data = json.load(data_file)
    s_db = ("axp"+ps+"_"+db).lower()
    USER_ID = data[s_db]['id']
    PASSWORD = data[s_db]['pwd']
    try:
        conn = pyodbc.connect(
            r'DSN=RDB'+db+ps[:-1]+';UID=' + USER_ID + ';PWD=' + PASSWORD)
        return conn
    except:
        print("輸入錯誤的資料")


def getRdbData(dataCount, dataTable, conn):
    if (dataCount == -1 or dataCount == 0):
        sqlstr = "select * from %s limit to 5000 rows" % dataTable.upper()
        cursor = conn.cursor()
        try:
            tStart = time.time()
            cursor.execute(sqlstr)
            row = cursor.fetchall()
            tEnd = time.time()
            print("讀取資料總共耗時:%f 秒" % (tEnd-tStart))
            return row
        except cx_Oracle.DatabaseError as er:
            print(er)
        

def check_contain_chinese(check_str, big5_Struct):
    #先檢查內容有包含中文資料的欄位，然後將該欄為的大小 x1.5 。
    #因為utf8的中文大小是big5的1.5倍 
    reg = re.compile(r'[0-9]+')
    idx = []
    filter_idx = {}
    for i in check_str:
        big5_Struct['Address'] = list(i)
        get_chinese_type = big5_Struct.loc[big5_Struct.iloc[:,2].str.contains(u'[\u4e00-\u9fa5]+', na=False),'type'] #有中文的欄位
        if (get_chinese_type.values.size>0):
            idx.append(get_chinese_type.index[0])
            if get_chinese_type.index[0] not in filter_idx:
                filter_idx = set(idx)
                big5_NumType = reg.search(get_chinese_type.values[0])
                utf8_DataType = math.ceil(int(big5_NumType.group(0))*1.5)
                big5_Struct.loc[get_chinese_type.index[0],'type'] = "CHAR ("+str(utf8_DataType)+")"
    return big5_Struct.drop(columns='Address')




class RdbToOracle:
    def __init__(self, conn, dataTable):
        self.conn = conn
        self.dataTable = dataTable
        self.rp547a = "tqc/tqc0213ora@rp547a"
        self.getRdbStruct()   #取得rdb資料結構為預設，為其他的def提供rdb的資料結構
    def oracle_CheckStruct(self):
        #檢查oracle資料表是否已建立

        self.row = getRdbData(-1, self.dataTable, self.conn)
        
        checked_struct = check_contain_chinese(self.row, self.struct)
        # if (checked_struct.any == True):
            # self.struct['type'] = checked_struct
        try:
            sqlstr = 'select count(*) from "PYTHON_'+self.dataTable.upper()+'"'
            conn_rp547a = cx_Oracle.connect(self.rp547a)
            cursor_rp547a = conn_rp547a.cursor()
            cursor_rp547a.execute(sqlstr)
            result_per = cursor_rp547a.fetchone()
            if (result_per[0] == 0):
                print("有近來")
                self.InsertOracleData(result_per[0])
        except cx_Oracle.DatabaseError as er:
            print("oracle資料表"+self.dataTable+"有錯誤=")
            x = er.args[0]
            print(x.message+"\n")
            if 'ORA-00942' in x.message:
                print("目前oracle資料表 python_"+self.dataTable+"沒創建，開始建立....")
                self.oracle_CreatStruct()
        conn_rp547a.close()

    def oracle_CreatStruct(self):
        #在oracle中建立RDB的資料表
        create_sql = 'create table "TQC"."PYTHON_%s" (' % self.dataTable.upper()
        for index, row in self.struct.iterrows():
            if "LOCK" in row['field_name'] and len(row['field_name'].strip()) == 4:
                create_sql += '"lock" '
            else:
                create_sql += '"%s" ' % row['field_name'].strip()
            create_sql += '%s ' % row['type'].strip()
            if "REAL" in row['type']:
                create_sql += "default 0.0,"
            elif "INTEGER" in row['type']:
                create_sql += "default 0,"
            else:
                create_sql += "default '' ,"
        create_sql = create_sql[:-1]+")"
        conn_rp547a = cx_Oracle.connect(self.rp547a)
        cursor_rp547a = conn_rp547a.cursor()   
        print(create_sql)
        try:
            cursor_rp547a.execute(create_sql)
            conn_rp547a.commit()
            print("create "+self.dataTable.upper()+"完成!")
            self.InsertOracleData(-1)
        except:
            print("oracle建立資料表失敗")
        conn_rp547a.close()
        
    def InsertOracleData(self, dataCount):
        #撈取RDB資料表中的資料，並存入oracle中
        insertsql = 'insert into TQC."PYTHON_%s" (' % self.dataTable.upper()
        placeholder = "("
        idx = 1
        for datas in self.struct['field_name']:
            if "LOCK" in datas and len(datas.strip()) == 4:
                insertsql += '"'+datas.strip().lower()+'",'
            else:
                insertsql += datas.strip()+","
            placeholder += ":"+str(idx)+","
            idx += 1
        placeholder = placeholder[:-1] + ")"
        insertsql = insertsql[:-1]+") VALUES " + placeholder #insert的語法
        try:
            conn_rp547a = cx_Oracle.connect(self.rp547a)
            cursor_rp547a = conn_rp547a.cursor()
            tStart = time.time()
            cursor_rp547a.executemany(insertsql, self.row)
            conn_rp547a.commit()
            tEnd = time.time()
            print("寫入資料總共耗時:%f 秒" % (tEnd-tStart))
            conn_rp547a.close()
        except cx_Oracle.DatabaseError as er:
            print("查無資料R" , er)
    def getRdbStruct(self):
        sqlstr = "SELECT rdb$field_name,"
        sqlstr += "(select UTIL_GET_DTYPE(RDB$FIELD_TYPE,RDB$FIELD_SCALE,RDB$FIELD_LENGTH, RDB$SEGMENT_LENGTH, RDB$FIELD_SUB_TYPE) "
        sqlstr += "from RDB$FIELDS where RDB$FIELD_NAME = rdb$relation_fields.RDB$FIELD_source)"
        sqlstr += "from rdb$relation_fields where rdb$relation_name = '%s'" % self.dataTable.upper()
        struct = pd.read_sql(sqlstr, self.conn)
        struct.rename(columns={"RDB$FIELD_NAME": "field_name", "": "type"}, inplace=True)
        self.struct = struct
        




    


if __name__ == '__main__':
    pnSys = input("請輸入系統別(36a或76a):")
    dataBase = input("請輸入RDB資料庫:")
    dataTable = input("請輸入RDB資料表:")

    # try:
    temp = checkRdbTable(pnSys, dataBase)
    RdbToOracleInstance = RdbToOracle(temp, dataTable)
    # except:
    #     print("===========================================")
    #     print("資料庫底下:"+dataBase+"\n無資料表:"+dataTable)
    #     exit()
    RdbToOracleInstance.oracle_CheckStruct()
    temp.close()
