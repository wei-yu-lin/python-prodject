from os import write
import pyodbc
import pandas as pd
import json
import time
import cx_Oracle


class RdbToOracle:
    def __init__(self, conn, dataTable):
        self.conn = conn
        self.dataTable = dataTable
        self.rp547b = "ecuser/ecuser@rp547b"
        self.getRdbStruct()   #取得rdb資料結構為預設，為其他的def提供rdb的資料結構
    def oracle_CheckStruct(self):
        #檢查oracle資料表是否已建立
        try:
            sqlstr = 'select count(*) from "python_'+self.dataTable+'"'
            conn_rp547b = cx_Oracle.connect(self.rp547b)
            cursor_rp547b = conn_rp547b.cursor()
            cursor_rp547b.execute(sqlstr)
            result_per = cursor_rp547b.fetchone()
            if (result_per[0] >= 0):
                print("有近來")
                self.InsertOracleData()
        except cx_Oracle.DatabaseError as er:
            print("oracle資料表"+self.dataTable+"有錯誤=")
            x = er.args[0]
            print(x.message+"\n")
            if 'ORA-00942' in x.message:
                print("目前oracle資料表 python_"+self.dataTable+"沒創建，開始建立....")
                self.oracle_CreatStruct()
        conn_rp547b.close()

    def oracle_CreatStruct(self):
        #在oracle中建立RDB的資料表
        
        create_sql = 'create table "ECUSER"."python_%s" (' % self.dataTable
        for index, row in self.struct.iterrows():
            create_sql += '"%s" ' % row['field_name'].strip()
            create_sql += '%s ' % row['type'].strip()
            if "REAL" in row['type']:
                create_sql += "default 0.0,"
            else:
                create_sql += "default '' ,"
        create_sql = create_sql[:-1]+")"

        conn_rp547b = cx_Oracle.connect(self.rp547b)
        cursor_rp547b = conn_rp547b.cursor()

        try:
            cursor_rp547b.execute(create_sql)
            conn_rp547b.commit()
            print("create "+self.dataTable.upper()+"完成!")
            self.InsertOracleData()
        except:
            print("oracle建立資料表失敗")
        conn_rp547b.close()
        
    def InsertOracleData(self):
        #撈取RDB資料表中的資料，並存入oracle中
        insertsql = 'insert into ECUSER."python_%s" (' % self.dataTable
        placeholder = "("
        idx = 1
        for datas in self.struct['field_name']:
            insertsql += datas.strip()+","
            placeholder += ":"+str(idx)+","
            idx += 1
        placeholder = placeholder[:-1] + ")"
        insertsql = insertsql[:-1]+") VALUES " + placeholder #insert的語法
        
        try:
            sqlstr = "select * from %s " %self.dataTable
            cursor = self.conn.cursor()
            try:
                tStart = time.time()
                cursor.execute(sqlstr)
                row = cursor.fetchall()
                tEnd = time.time()
                print("讀取資料總共耗時:%f 秒" % (tEnd-tStart))
            except cx_Oracle.DatabaseError as er:
                print(er)
            conn_rp547b = cx_Oracle.connect(self.rp547b)
            cursor_rp547b = conn_rp547b.cursor()
            tStart = time.time()
            cursor_rp547b.executemany(insertsql, row)
            conn_rp547b.commit()
            tEnd = time.time()
            print("寫入資料總共耗時:%f 秒" % (tEnd-tStart))
            conn_rp547b.close()
        except cx_Oracle.DatabaseError as er:
            print("查無資料R" , er)
    def getRdbStruct(self):
        sqlstr = "SELECT rdb$field_name,"
        sqlstr += "(select UTIL_GET_DTYPE(RDB$FIELD_TYPE,RDB$FIELD_SCALE,RDB$FIELD_LENGTH, RDB$SEGMENT_LENGTH, RDB$FIELD_SUB_TYPE) "
        sqlstr += "from RDB$FIELDS where RDB$FIELD_NAME = rdb$relation_fields.RDB$FIELD_source)"
        sqlstr += "from rdb$relation_fields where rdb$relation_name ='CCAP210M'"
        struct = pd.read_sql(sqlstr, self.conn)
        struct.rename(columns={"RDB$FIELD_NAME": "field_name", "": "type"}, inplace=True)
        self.struct = struct


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
        raise "輸入錯誤的資料"


if __name__ == '__main__':
    pnSys = input("請輸入系統別(36a或76a):")
    dataBase = input("請輸入RDB資料庫:")
    dataTable = input("請輸入RDB資料表:")

    try:
        temp = checkRdbTable(pnSys, dataBase)
        RdbToOracleInstance = RdbToOracle(temp, dataTable)
    except:
        print("===========================================")
        print("資料庫底下:"+dataBase+"\n無資料表:"+dataTable)
        exit()
    RdbToOracleInstance.oracle_CheckStruct()
    temp.close()
