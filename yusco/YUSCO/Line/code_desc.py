from ..Core.DB_RDB import RDBConn
from YUSCO.Core.DB_ORACLE import OracleDB_dic2
import pyodbc
import cx_Oracle


# 客戶代碼
def db_orda011m(cust_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('ORD'))
        s_sql = "select short_name from orda010m where cust_no ='" + cust_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

# APN_NO 代碼
def db_micm060m(apn_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('MIC'))
        s_sql = "select remark from micm060m where code_type = '05' and code ='" + apn_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

#主要缺陷並轉成中文說明
def get_deffect_Description(main_deff):

    extent_desc = ''
    conn = cx_Oracle.connect(OracleDB_dic2('RP547B_ECUSER'))
    s_sql = "select cdesc  from MISCODE where ckind ='DC' and status ='Y' and code ='" + main_deff[1:4] + "'"
    cursor = conn.cursor()
    try:
        cursor.execute(s_sql)
        deff_desc = cursor.fetchone()[0]
    except cx_Oracle.DatabaseError as e:
        deff_desc = '不明缺陷'
        print(s_sql + "\n")
        print(str(e))
        cursor.close()
        conn.close()

    d_extent = main_deff[14:15]
    extent_desc = ''
    if d_extent == 'F':
        extent_desc = '極輕微'
    elif d_extent == 'H':
        extent_desc = '嚴重'
    elif d_extent == 'L':
        extent_desc = '輕微'
    elif d_extent == 'S':
        extent_desc = '極嚴重'
    elif d_extent == 'M':
        extent_desc = '中等'

    deff_extent_desc = str(deff_desc) + str(extent_desc)

    return deff_extent_desc 

