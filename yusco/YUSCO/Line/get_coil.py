from ..Core.DB_RDB import RDBConn
from YUSCO.Line.code_desc import db_orda011m, db_micm060m
import pyodbc
import pandas as pd


def db_pcmb020m(coil_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('PCM'))
        s_sql = "select coil_no,curr_station,defact01,cb_first_order_item from pcmb020m where coil_no ='" + coil_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

def db_pcmb025h(coil_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('PCM'))
        s_sql = "select coil_no,product_code,defact01,cb_first_order_item  from pcmb025h where coil_no ='" + coil_no + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

def db_pcmb030m(coil_no, station):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('PCM'))
        if station == 'ALL':
            coil_no_8 = coil_no[0:8]
            coil_no_9 = coil_no[0:9]
            coil_no_10 = coil_no[0:10]
            coil_no_11 = coil_no[0:11]
            s_sql = (
                    " select "  
                    " coil_no,schd_no,station,oper_code,last_prod_date,shift_date "
                    " from pcmb030m "
                    " where "
                    " coil_no='" + coil_no_8 + "' or coil_no='" + coil_no_9 + "' or coil_no='" + coil_no_10 + "' or coil_no='" + coil_no_11 + "'"
                    " order by last_prod_date asc"
            )
        else:
            s_sql = "select coil_no,schd_no,station,last_prod_date from pcmb030m where coil_no ='" + coil_no + "' and station='" + station + "'" 

        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

def db_wipb040_041h(coil_no):
    result = []
    coil_no_8 = coil_no[0:8]
    coil_no_9 = coil_no[0:9]
    coil_no_10 = coil_no[0:10]
    coil_no_11 = coil_no[0:11]
    try:
        conn = pyodbc.connect(RDBConn('WIP'))
        s_sql = (
                " select "  
                " a.coil_no, a.station, a.schd_no, a.date_last_maint, a.class_code, a.qc_remark, a.defect_code1, "
                " b.cycle_1 from wipb040h a , wipb041h b "
                " where (a.coil_no = b.coil_no and a.station = b.station and a.schd_no = b.schd_no) "
                " and (a.coil_no='" + coil_no_8 + "' or a.coil_no='" + coil_no_9 + "' or a.coil_no='" + coil_no_10 + "' or a.coil_no='" + coil_no_11 + "')"
        )
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

def db_shpa011m(coil_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('SHP'))
        s_sql = ( 
                " select "
                " product_id, product_code, ship_no, order_no_item, item_weight,"
                " prod_thick "
                " from shpa011m where product_id ='" + coil_no + "'"
        )
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result

def db_tqcl500m(coil_no, product_code):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('TQC'))
        s_sql = "select test_id from tqcl500m where product_id ='" + coil_no + "' and product_code = '" + product_code + "'"
        result = list(conn.execute(s_sql))
        conn.close()
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result


def db_tqcl010mPandas(test_id, product_code):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('TQC'))
        s_sql = (
                " select "
                " product_id, ave_ts , ave_ys_02 ,ave_ys_10 ,yield_elongation ,"
                " ave_elongation ,ave_hard_hrb, ave_hard_hv "
                " from tqcl010m where product_id ='" + test_id + "' and product_code = '" + product_code + "'"
        )
        df = pd.read_sql_query(s_sql,con=conn)
        if df.empty:
            s_sql = (
                    " select "
                    " product_id, ave_ts , ave_ys_02 ,ave_ys_10 ,yield_elongation ,"
                    " ave_elongation ,ave_hard_hrb, ave_hard_hv "
                    " from tqcl050m where product_id ='" + test_id + "' and product_code = '" + product_code + "'"
            )
            df = pd.read_sql_query(s_sql,con=conn)
        conn.close()
        result = df
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result


def db_ordb011mPandas(order_no_item):
    result = []
    cust_name = ''
    apn_desc = ''
    try:
        conn = pyodbc.connect(RDBConn('ORD'))
        s_sql = (
                " select "
                " order_no_item, "  
                " (select cust_no from ordb010m where order_no = ordb011m.order_no) as cust_no, "
                " order_thick_min, order_thick_aim, order_thick_max, "
                " order_width_min, order_width_aim, order_width_max, "
                " unit_weight_max, unit_weight_min, "
                " unit_price, apn_no , "
                " special_require, ordb011m_remark "
                " from ordb011m where order_no_item = '" + order_no_item + "'"
        )
        df = pd.read_sql_query(s_sql,con=conn)
        conn.close()
        if not df.empty:
            cust_no =df['CUST_NO'][0].strip()
            apn_no =df['APN_NO'][0].strip()
            print(cust_no, apn_no)
            if cust_no != '':
                rsA = db_orda011m(cust_no)
                if rsA:
                    cust_name = rsA[0][0]
            if apn_no != '':
                rsA = db_micm060m(apn_no)
                if rsA:
                    apn_desc = rsA[0][0].strip()
            df['CUST_NO'] = cust_no + "(" + cust_name + ")"
            df['APN_NO'] = apn_no + "(" + apn_desc + ")"
            print(df)
        result = df
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result


def db_wipb040_041Pandas(coil_no, station, schd_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('WIP'))
        s_sql = (
                " select "  
                " a.coil_no , a.station, a.date_last_maint, a.class_code, "
                " a.meas_coil_thick01, a.meas_coil_thick02, a.meas_coil_thick03, a.meas_coil_thick04, a.meas_coil_thick05, "
                " a.meas_coil_wid01, a.meas_coil_wid02, a.meas_coil_wid03, a.meas_coil_wid04, a.meas_coil_wid05,  "
                " a.defect_code1, a.defect_code2, a.defect_code3, a.defect_code4, a.defect_code5, "
                " a.defect_code6, a.defect_code7, a.defect_code8, a.defect_code9, a.defect_code10, "
                " b.defect_code11, b.defect_code12, b.defect_code13, b.defect_code14, b.defect_code15, "
                " b.defect_code16, b.defect_code17, b.defect_code18, "
                " b.cycle_1, b.cycle_2, b.cycle_3, b.cycle_4, b.cycle_5, "
                " b.cycle_6, b.cycle_7, b.cycle_8, b.cycle_9, b.cycle_10, "
                " b.cycle_11, b.cycle_12, b.cycle_13, b.cycle_14, b.cycle_15, "
                " b.cycle_16, b.cycle_17, b.cycle_18, "
                " b.sort_1, b.sort_2, b.sort_3, b.sort_4, b.sort_5, "
                " b.sort_6, b.sort_7, b.sort_8, b.sort_9, b.sort_10, "
                " b.sort_11, b.sort_12, b.sort_13, b.sort_14, b.sort_15, "
                " b.sort_16, b.sort_17, b.sort_18, "
                " a.gloss_h, a.gloss_m, a.gloss_e, a.gloss_h1, a.gloss_m1 "
                " from wipb040h a , wipb041h b "
                " where (a.coil_no = b.coil_no and a.station = b.station and a.schd_no = b.schd_no) "
                " and (a.coil_no='" + coil_no + "' and a.station = '" + station + "' and a.schd_no = '" + schd_no + "')"
        )
        df = pd.read_sql_query(s_sql,con=conn)
#        print(df)
        conn.close()
        result = df

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result


def db_pcmb030mPandas(coil_no):
    result = []
    try:
        conn = pyodbc.connect(RDBConn('PCM'))
        coil_no_8 = coil_no[0:8]
        coil_no_9 = coil_no[0:9]
        coil_no_10 = coil_no[0:10]
        coil_no_11 = coil_no[0:11]
        s_sql = (
                " select "  
                " coil_no, oper_code, last_prod_date, coil_thick, coil_width, "
                " coil_weight, coil_in_diam, coil_out_diam, ic_code, edging, "
                " class_code "
                " from pcmb030m "
                " where "
                " coil_no='" + coil_no_8 + "' or coil_no='" + coil_no_9 + "' or coil_no='" + coil_no_10 + "' or coil_no='" + coil_no_11 + "'"
                " order by last_prod_date asc"
        )

        df = pd.read_sql_query(s_sql,con=conn)
        conn.close()
        result = df
#        print(df)
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return result
