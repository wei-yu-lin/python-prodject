import pyodbc
import pandas as pd
import json
import time
import math
import cx_Oracle
import math
import re
startTime = time.time()


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


def getRdbData( dataTable, conn):
    sqlstr = "select * from %s" % dataTable.upper()
    try:
        tStart = time.time()
        row = pd.read_sql_query(sqlstr,conn)
        df_dtype = row.select_dtypes(['object'])
        row[df_dtype.columns] = df_dtype.apply(lambda x:x.str.strip())
        tEnd = time.time()
        print("讀取資料總共花時:%f 秒" % (tEnd-tStart))
        return row
    except cx_Oracle.DatabaseError as er:
        print(er)
        

def check_contain_chinese(check_str, big5_Struct):
    #先檢查內容有包含中文資料的欄位，然後將該欄為的大小 x1.5 。
    #因為utf8的中文大小是big5的1.5倍 
    reg = re.compile(r'[0-9]+')
    filter_type = {}
    data = []
    for i in check_str:
        big5_Struct['newWave'] = list(i)
        data.append([x for x in i])   
        get_chinese_type = big5_Struct.loc[big5_Struct.iloc[:,2].str.contains(u'[\u4e00-\u9fa5]+', na=False),'type'] #有中文的欄位
        ggg = get_chinese_type.to_dict()
        val1 = [x for x in filter_type.keys()]
        
        for (k,v) in ggg.items():
            if k not in val1:
                filter_type.update({k:v})
                big5_NumType = reg.search(v)
                utf8_DataType = math.ceil(int(big5_NumType.group(0))*1.5)
                big5_Struct.loc[k,'type'] = "CHAR ("+str(utf8_DataType)+")"
        # with open('news.txt','w+') as f:
        #     f.write(str(data))
    return big5_Struct.drop(columns='newWave')




class RdbToOracle:
    def __init__(self, conn, dataTable):
        self.conn = conn
        self.dataTable = dataTable
        self.rp547b = "YUPCMSYS/PCM62440@rp547b"
        self.getRdbStruct()   #取得rdb資料結構為預設，為其他的def提供rdb的資料結構
    def oracle_CheckStruct(self):
        #檢查oracle資料表是否已建立.
        try:
            sqlstr = 'select count(*) from "YUPCMSYS"."'+self.dataTable.upper()+'"'
            conn_rp547b = cx_Oracle.connect(self.rp547b)
            cursor_rp547b = conn_rp547b.cursor()
            cursor_rp547b.execute(sqlstr)
            result_per = cursor_rp547b.fetchone()
            if (result_per[0] == 0):
                self.row = getRdbData( self.dataTable, self.conn)
                self.InsertOracleData()
            else:
                print("請清空資料表"+self.dataTable + str(result_per[0]))
                return
        except cx_Oracle.DatabaseError as er:
            x = er.args[0]
            print(x.message)
            if 'ORA-00942' in x.message:
                print("目前oracle資料表 "+self.dataTable+"沒創建，開始建立....")
                self.row = getRdbData( self.dataTable, self.conn)
                checked_struct = check_contain_chinese(self.row, self.struct)
                if (checked_struct.any == True):
                    self.struct['type'] = checked_struct
                self.oracle_CreatStruct()
                self.InsertOracleData()
        conn_rp547b.close()

    def oracle_CreatStruct(self):
        #在oracle中建立RDB的資料表
        create_sql = 'create table "YUPCMSYS"."%s" (' % self.dataTable.upper()
        for index, row in self.struct.iterrows():
            if "LOCK" in row['field_name'] and len(row['field_name'].strip()) == 4:
                create_sql += '"lock" '
            else:
                create_sql += '"%s" ' % row['field_name'].strip()
            if "DATE VMS" in row['type']:
                create_sql += 'DATE '
            elif "TINYINT" in row['type'] or "SMALLINT" in row['type']:
                create_sql += 'NUMBER(5,0) '
            elif "BIGINT" in row['type']:
                create_sql += 'NUMBER(20,0) '
            elif "CHAR" in row['type']:
                create_sql += row['type'].replace("CHAR","VARCHAR2")+' '
            elif "INTEGER" in row['type']:
                create_sql += 'NUMBER(10,0) '
            else:
                create_sql += '%s ' % row['type'].strip()
            if "REAL" in row['type']:
                create_sql += "default 0.0,"
            elif ("INTEGER" in row['type']) or ("SMALLINT" in row['type']):
                create_sql += "default 0,"
            else:
                create_sql += "default '' ,"
        create_sql = create_sql[:-1]+")"
        conn_rp547b = cx_Oracle.connect(self.rp547b)
        cursor_rp547b = conn_rp547b.cursor()   
        print(create_sql)
        try:
            cursor_rp547b.execute(create_sql)
            conn_rp547b.commit()
            print("create "+self.dataTable.upper()+"完成!")
        except pyodbc.Error as ex:
            sqlstate = ex.args[0]
            print("sqlstate=",sqlstate)
        
        conn_rp547b.close()
        
    def InsertOracleData(self):
        
        
        #撈取RDB資料表中的資料，並存入oracle中
        insertsql = 'insert into "YUPCMSYS"."%s" (' % self.dataTable.upper()
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
            
            conn_rp547b = cx_Oracle.connect(self.rp547b)
            cursor_rp547b = conn_rp547b.cursor()
            num_bytes_in_chunk = 100000
            rowLength = len(self.row.values.tolist())
            tStart = time.time()
            # print("資料長度=",str(rowLength)+" 相除=",str(math.ceil(rowLength/num_bytes_in_chunk)))
            for i in range(math.ceil(rowLength/num_bytes_in_chunk)):
                if(i==0):
                    cursor_rp547b.executemany(insertsql, self.row.values.tolist()[1:num_bytes_in_chunk])
                    # print('第一',"1:"+str(num_bytes_in_chunk))
                elif(i == (math.ceil(rowLength/num_bytes_in_chunk)-1) ):
                    cursor_rp547b.executemany(insertsql, self.row.values.tolist()[num_bytes_in_chunk*i:-1])
                    # print('第三',str(num_bytes_in_chunk*i)+":"+str(rowLength))
                else:
                    cursor_rp547b.executemany(insertsql, self.row.values.tolist()[num_bytes_in_chunk*i:num_bytes_in_chunk*(i+1)])
                    # print('第二',str(num_bytes_in_chunk*i)+":"+str(num_bytes_in_chunk*(i+1)))

            conn_rp547b.commit()
            tEnd = time.time()
            print("寫入資料總共花時:%f 秒" % (tEnd-tStart))
            conn_rp547b.close()
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
    temp = checkRdbTable(pnSys, dataBase)
    RdbToOracleInstance = RdbToOracle(temp, dataTable)
    
    RdbToOracleInstance.oracle_CheckStruct()
    
    temp.close()
    endTime = time.time()
    print("執行程式總花費時間", endTime - startTime )