import pyodbc
import pandas as pd
import os
import time
import cx_Oracle
from sqlalchemy import create_engine

conn = pyodbc.connect(r'DSN=RDBCPS36;UID=yucps00;PWD=cps111036a')
sqlstr = "SELECT rdb$field_name,"
sqlstr += "(select UTIL_GET_DTYPE(RDB$FIELD_TYPE,RDB$FIELD_SCALE,RDB$FIELD_LENGTH, RDB$SEGMENT_LENGTH, RDB$FIELD_SUB_TYPE) "
sqlstr += "from RDB$FIELDS where RDB$FIELD_NAME = rdb$relation_fields.RDB$FIELD_source)"
sqlstr += "from rdb$relation_fields where rdb$relation_name ='CCAP210M'"
struct = pd.read_sql(sqlstr, conn)
struct.rename(
    columns={"RDB$FIELD_NAME": "field_name", "": "type"}, inplace=True)
conn.close()

insertsql = 'insert into ECUSER."python_ccap210m" ('
placeholder = "("
idx = 1
for datas in struct['field_name']:
    insertsql += datas.strip()+","
    placeholder += ":"+str(idx)+","
    idx += 1
placeholder = placeholder[:-1] + ")"
insertsql = insertsql[:-1]+") VALUES " + placeholder 



conn = pyodbc.connect(r'DSN=RDBCPS36;UID=yucps00;PWD=cps111036a')
cursor = conn.cursor()
tStart = time.time()
cursor.execute("select * from ccap210m")
row = cursor.fetchall()
tEnd = time.time()
conn.close
print("讀取資料總共耗時:%f 秒" % (tEnd-tStart))

conn_rp547b = cx_Oracle.connect("ecuser/ecuser@rp547b")
cursor_rp547b = conn_rp547b.cursor()
tStart = time.time()
cursor_rp547b.executemany(insertsql, row)
conn_rp547b.commit()
tEnd = time.time()
print("寫入資料總共耗時:%f 秒" % (tEnd-tStart))
conn_rp547b.close()
