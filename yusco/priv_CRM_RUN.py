import pyodbc
import pandas as pd
import openpyxl
"""
整理冷軋運轉日報表的權限

先去EF2搜尋申請表單裡面有CRM_RUN或CRMRUN的申請人，這些申請人再回去比對EXCEL檔(資料表彙整出來)裡面的人員。
如果有，則將當初他們有在EXCEL裡面的產線、權限...等，寫入新的EXCEL檔裡
"""
dsn_EF2 = 'DRIVER={SQL Server};SERVER=100.1.1.23;DATABASE=EF2KWeb;UID=yud222;PWD=yud222'
conn_EF2 = pyodbc.connect(dsn_EF2)
strsql = "select oxa38a002 from oxa38a inner join resda on oxa38a001 = resda001 and oxa38a002 = resda002 inner join resak on resak001 = oxa38a008 where oxa38a005 >= '2021/02/01' and oxa38a005 <= '2021/03/03' and oxa38a007 = 'CRMW' and oxa38a008 = '65426' and resda020='3' and resda021='2' order by oxa38a008,oxa38a007s"
data = pd.read_sql(strsql, conn_EF2)
一廠權限 = pd.read_excel("excel\haps010m.xlsx")
二廠權限 = pd.read_excel("excel\haps020m.xlsx")
一廠工號 = set(一廠權限['user_id'].str.strip())
二廠工號 = set(二廠權限['user_id'].str.strip())
writer1 = pd.ExcelWriter('excel\冷軋一廠.xlsx')
writer2 = pd.ExcelWriter('excel\冷軋二廠.xlsx')
start_row1 = 0
start_row2 = 0
for items in data['oxa38a002']:
    s_sql = "select oxa38b004 "
    s_sql = s_sql + "from oxa38b where oxa38b001='oxa38' and oxa38b002='" + \
        items+"' and (oxa38b021 = 'CRM_RUN' or oxa38b021 = 'CRMRUN')"
    Requisition = pd.read_sql(s_sql, conn_EF2)
    if not (Requisition.empty):
        set_Requisition = set("YU"+(Requisition['oxa38b004']))
        crm1_user = set_Requisition & 一廠工號
        crm2_user = set_Requisition & 二廠工號

        if (crm1_user):
            for temp in crm1_user:
                tp = 一廠權限[一廠權限.user_id.str.strip() == temp]
                tp.to_excel(writer1, index=False, startrow=start_row1)
                start_row1 = start_row1 + len(tp) + 1

        if (crm2_user):
            for temp in crm2_user:
                tp2 = 二廠權限[二廠權限.user_id.str.strip() == temp]
                tp2.to_excel(writer2, index=False, startrow=start_row2)
                start_row2 = start_row2 + len(tp2) + 1
        if not (set_Requisition & 一廠工號):
            if not (set_Requisition & 二廠工號):
                print(set_Requisition)

writer1.save()
writer1.close()
writer2.save()
writer2.close()
conn_EF2.close()
