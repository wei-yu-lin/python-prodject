from YUSCO.Line.get_coil import db_wipb040_041h, db_wipb040_041Pandas, db_ordb011mPandas, db_ordb011mPandas, db_tqcl010mPandas, db_pcmb030mPandas
from YUSCO.Util.render_table import render_mpl_table
from YUSCO.Util.comm_code import OperCode_dic
import pandas as pd
import matplotlib.pyplot as plt
import os


def coil_status_rep(coil_no):
    status = False
    coil_list = []
    schd_list = []
    station_list = []
    date_list = []
    defect01_list = []
    try:
        resultA = db_wipb040_041h(coil_no)
        for i1,i2 in enumerate(resultA):
            coil_list.append(resultA[i1][0])
            schd_list.append(resultA[i1][2])
            station_list.append(resultA[i1][1])
            date_list.append(resultA[i1][3])
            defect01_list.append(resultA[i1][6])

        df = pd.DataFrame()
        df['coil_no'] = coil_list
        df['schd_no'] = schd_list
        df['station'] = station_list
        df['prod_date'] = date_list
        df['defect01'] = defect01_list


        render_mpl_table(df, header_columns=0, col_width=3.0)
        root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
        plt.savefig( root_path + coil_no + 'Table.png')
        print(root_path + coil_no +'Table.png' )
        status = True
    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return status 


def coil_wip_report(coil_no,station,schd_no):
# 圖片名稱不加入schd_no , 因為有些是星號,會導致圖片無法產生
    status = False
    try:
        df = db_wipb040_041Pandas(coil_no,station,schd_no)
        if not df.empty:
            df['DEFECT1'] = df['DEFECT_CODE1'][0] + '　　　' + str(df['CYCLE_1'][0]) + '　　　' + str(df['SORT_1'][0])
            df['DEFECT2'] = df['DEFECT_CODE2'][0] + '　　　' + str(df['CYCLE_2'][0]) + '　　　' + str(df['SORT_2'][0])
            df['DEFECT3'] = df['DEFECT_CODE3'][0] + '　　　' + str(df['CYCLE_3'][0]) + '　　　' + str(df['SORT_3'][0])
            df['DEFECT4'] = df['DEFECT_CODE4'][0] + '　　　' + str(df['CYCLE_4'][0]) + '　　　' + str(df['SORT_4'][0])
            df['DEFECT5'] = df['DEFECT_CODE5'][0] + '　　　' + str(df['CYCLE_5'][0]) + '　　　' + str(df['SORT_5'][0])
            df['DEFECT6'] = df['DEFECT_CODE6'][0] + '　　　' + str(df['CYCLE_6'][0]) + '　　　' + str(df['SORT_6'][0])
            df['DEFECT7'] = df['DEFECT_CODE7'][0] + '　　　' + str(df['CYCLE_7'][0]) + '　　　' + str(df['SORT_7'][0])
            df['DEFECT8'] = df['DEFECT_CODE8'][0] + '　　　' + str(df['CYCLE_8'][0]) + '　　　' + str(df['SORT_8'][0])
            df['DEFECT9'] = df['DEFECT_CODE9'][0] + '　　　' + str(df['CYCLE_9'][0]) + '　　　' + str(df['SORT_9'][0])
            df['DEFECT10'] = df['DEFECT_CODE10'][0] + '　　　' + str(df['CYCLE_10'][0]) + '　　　' + str(df['SORT_10'][0])
            df['DEFECT11'] = df['DEFECT_CODE11'][0] + '　　　' + str(df['CYCLE_11'][0]) + '　　　' + str(df['SORT_11'][0])
            df['DEFECT12'] = df['DEFECT_CODE12'][0] + '　　　' + str(df['CYCLE_12'][0]) + '　　　' + str(df['SORT_12'][0])
            df['DEFECT13'] = df['DEFECT_CODE13'][0] + '　　　' + str(df['CYCLE_13'][0]) + '　　　' + str(df['SORT_13'][0])
            df['DEFECT14'] = df['DEFECT_CODE14'][0] + '　　　' + str(df['CYCLE_14'][0]) + '　　　' + str(df['SORT_14'][0])
            df['DEFECT15'] = df['DEFECT_CODE15'][0] + '　　　' + str(df['CYCLE_15'][0]) + '　　　' + str(df['SORT_15'][0])
            df['DEFECT16'] = df['DEFECT_CODE16'][0] + '　　　' + str(df['CYCLE_16'][0]) + '　　　' + str(df['SORT_16'][0])
            df['DEFECT17'] = df['DEFECT_CODE17'][0] + '　　　' + str(df['CYCLE_17'][0]) + '　　　' + str(df['SORT_17'][0])
            df['DEFECT18'] = df['DEFECT_CODE18'][0] + '　　　' + str(df['CYCLE_18'][0]) + '　　　' + str(df['SORT_18'][0])
            df.__delitem__('DEFECT_CODE1')
            df.__delitem__('DEFECT_CODE2')
            df.__delitem__('DEFECT_CODE3')
            df.__delitem__('DEFECT_CODE4')
            df.__delitem__('DEFECT_CODE5')
            df.__delitem__('DEFECT_CODE6')
            df.__delitem__('DEFECT_CODE7')
            df.__delitem__('DEFECT_CODE8')
            df.__delitem__('DEFECT_CODE9')
            df.__delitem__('DEFECT_CODE10')
            df.__delitem__('DEFECT_CODE11')
            df.__delitem__('DEFECT_CODE12')
            df.__delitem__('DEFECT_CODE13')
            df.__delitem__('DEFECT_CODE14')
            df.__delitem__('DEFECT_CODE15')
            df.__delitem__('DEFECT_CODE16')
            df.__delitem__('DEFECT_CODE17')
            df.__delitem__('DEFECT_CODE18')
            df.__delitem__('CYCLE_1')
            df.__delitem__('CYCLE_2')
            df.__delitem__('CYCLE_3')
            df.__delitem__('CYCLE_4')
            df.__delitem__('CYCLE_5')
            df.__delitem__('CYCLE_6')
            df.__delitem__('CYCLE_7')
            df.__delitem__('CYCLE_8')
            df.__delitem__('CYCLE_9')
            df.__delitem__('CYCLE_10')
            df.__delitem__('CYCLE_11')
            df.__delitem__('CYCLE_12')
            df.__delitem__('CYCLE_13')
            df.__delitem__('CYCLE_14')
            df.__delitem__('CYCLE_15')
            df.__delitem__('CYCLE_16')
            df.__delitem__('CYCLE_17')
            df.__delitem__('CYCLE_18')
            df.__delitem__('SORT_1')
            df.__delitem__('SORT_2')
            df.__delitem__('SORT_3')
            df.__delitem__('SORT_4')
            df.__delitem__('SORT_5')
            df.__delitem__('SORT_6')
            df.__delitem__('SORT_7')
            df.__delitem__('SORT_8')
            df.__delitem__('SORT_9')
            df.__delitem__('SORT_10')
            df.__delitem__('SORT_11')
            df.__delitem__('SORT_12')
            df.__delitem__('SORT_13')
            df.__delitem__('SORT_14')
            df.__delitem__('SORT_15')
            df.__delitem__('SORT_16')
            df.__delitem__('SORT_17')
            df.__delitem__('SORT_18')
            get_m_deff = df['DEFECT1'][0][0:15]

            col_ren = { 'COIL_NO':'捲號','STATION':'產線','DATE_LAST_MAINT':'維護日期','CLASS_CODE':'等級',
                        'MEAS_COIL_THICK01':'量測厚度1','MEAS_COIL_THICK02':'量測厚度2','MEAS_COIL_THICK03':'量測厚度3','MEAS_COIL_THICK04':'量測厚度4','MEAS_COIL_THICK05':'量測厚度5',
                        'MEAS_COIL_WID01':'量測寬度1','MEAS_COIL_WID02':'量測寬度2','MEAS_COIL_WID03':'量測寬度3','MEAS_COIL_WID04':'量測寬度4','MEAS_COIL_WID05':'量測寬度5',
                        'DEFECT1':'缺陷 週期 類別1','DEFECT2':'缺陷 週期 類別2','DEFECT3':'缺陷 週期 類別3','DEFECT4':'缺陷 週期 類別4','DEFECT5':'缺陷 週期 類別5',
                        'DEFECT6':'缺陷 週期 類別6','DEFECT7':'缺陷 週期 類別7','DEFECT8':'缺陷 週期 類別8','DEFECT9':'缺陷 週期 類別9','DEFECT10':'缺陷 週期 類別10', 
                        'DEFECT11':'缺陷 週期 類別11','DEFECT12':'缺陷 週期 類別12','DEFECT13':'缺陷 週期 類別13','DEFECT14':'缺陷 週期 類別14','DEFECT15':'缺陷 週期 類別15',
                        'DEFECT16':'缺陷 週期 類別16','DEFECT17':'缺陷 週期 類別17','DEFECT18':'缺陷 週期 類別18' 
                      }

#            col_ren = { 'COIL_NO':'捲號','STATION':'產線','DATE_LAST_MAINT':'維護日期','CLASS_CODE':'等級',
#                        'MEAS_COIL_THICK01':'量測厚度1','MEAS_COIL_THICK02':'量測厚度2','MEAS_COIL_THICK03':'量測厚度3','MEAS_COIL_THICK04':'量測厚度4','MEAS_COIL_THICK05':'量測厚度5',
#                        'MEAS_COIL_WID01':'量測寬度1','MEAS_COIL_WID02':'量測寬度2','MEAS_COIL_WID03':'量測寬度3','MEAS_COIL_WID04':'量測寬度4','MEAS_COIL_WID05':'量測寬度5',
#                        'DEFECT_CODE1':'缺陷1','DEFECT_CODE2':'缺陷2','DEFECT_CODE3':'缺陷3','DEFECT_CODE4':'缺陷4','DEFECT_CODE5':'缺陷5',
#                        'DEFECT_CODE6':'缺陷6','DEFECT_CODE7':'缺陷7','DEFECT_CODE8':'缺陷8','DEFECT_CODE9':'缺陷9','DEFECT_CODE10':'缺陷10',
#                        'DEFECT_CODE11':'缺陷11','DEFECT_CODE12':'缺陷12','DEFECT_CODE13':'缺陷13','DEFECT_CODE14':'缺陷14','DEFECT_CODE15':'缺陷15',
#                        'DEFECT_CODE16':'缺陷16','DEFECT_CODE17':'缺陷17','DEFECT_CODE18':'缺陷18',
#                        'CYCLE_1':'週期1','CYCLE_2':'週期2','CYCLE_3':'週期3','CYCLE_4':'週期4','CYCLE_5':'週期5',
#                        'CYCLE_6':'週期6','CYCLE_7':'週期7','CYCLE_8':'週期8','CYCLE_9':'週期9','CYCLE_10':'週期10',
#                        'CYCLE_11':'週期11','CYCLE_12':'週期12','CYCLE_13':'週期13','CYCLE_14':'週期14','CYCLE_15':'週期15',
#                        'CYCLE_16':'週期16','CYCLE_17':'週期17','CYCLE_18':'週期18',
#                        'SORT_1':'類別1','SORT_2':'類別2','SORT_3':'類別3','SORT_4':'類別4','SORT_5':'類別5',
#                        'SORT_6':'類別6','SORT_7':'類別7','SORT_8':'類別8','SORT_9':'類別9','SORT_10':'類別10',
#                        'SORT_11':'類別11','SORT_12':'類別12','SORT_13':'類別13','SORT_14':'類別14','SORT_15':'類別15',
#                        'SORT_16':'類別16','SORT_17':'類別17','SORT_18':'類別18',
#                        'DEFECT1':'缺陷 週期 類別1'
#                      }

            df.rename(columns=col_ren, inplace=True)       

            sf = df.transpose()[0]
            result_wip = pd.DataFrame({'column':sf.index, 'value':sf.values})
#           處理小數位數的問題
#            decimals = pd.Series([2], index=['value'])
#            result_wip = result_wip.round(decimals)
            print(result_wip)
            render_mpl_table(result_wip, header_columns=0, col_width=5.0)
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
            plt.savefig( root_path + 'WIP' + coil_no + station + 'Report.png')
            print(root_path + 'WIP' + coil_no + station +  'Report.png' )
            status = True
        else:
            print("wip找不到紀錄")

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))
    return status, get_m_deff

def coil_order_rep(order_no_item):
    status = False
    try:
        df = db_ordb011mPandas(order_no_item)

        if not df.empty:
            col_ren = { 
                        'ORDER_NO_ITEM':'訂單編號',
                        'ORDER_THICK_MIN':'厚度下限','ORDER_THICK_AIM':'厚度目標','ORDER_THICK_MAX':'厚度上限',
                        'ORDER_WIDTH_MIN':'寬度下限','ORDER_WIDTH_AIM':'寬度目標','ORDER_WIDTH_MAX':'寬度上限',
                        'UNIT_WEIGHT_MAX':'重量上限','UNIT_WEIGHT_MIN':'重量下限',
                        'UNIT_PRICE':'售價', 'APN_NO':'用途碼', 'CUST_NO':'客戶名稱',
                        'SPECIAL_REQUIRE':'特殊需求', 'ORDB011M_REMARK':'訂單備註'
                      }
            df.rename(columns=col_ren, inplace=True)            
            
            sf = df.transpose()[0]
            result_ord = pd.DataFrame({'column':sf.index, 'value':sf.values})
#            result_ord[['value']] = result_ord[['value']].astype(int)
#           處理小數位數的問題
            decimals = pd.Series([2], index=['value'])
            result_ord = result_ord.round(decimals)

            render_mpl_table(result_ord, header_columns=0, col_width=6.0)
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
            plt.savefig( root_path + 'ORD' + order_no_item + 'Report.png')
            print(root_path + 'ORD' + order_no_item + 'Report.png' )
            status = True
        else:
            print("ordb011m 找不到資料")

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return status 


def coil_tqc_report(test_id,product_code):
    status = False
    try:
        df = db_tqcl010mPandas(test_id, product_code)
        if not df.empty:
            col_ren = { 'PRODUCT_ID':'測試編號','AVE_TS':'抗拉強度','YIELD_ELONGATION':'降伏伸長率','AVE_ELONGATION':'伸長率',
                        'AVE_HARD_HRB':'硬度值HRB','AVE_HARD_HV':'硬度值HV'
                      }
            df.rename(columns=col_ren, inplace=True)            

            sf = df.transpose()[0]
            result_tqc = pd.DataFrame({'column':sf.index, 'value':sf.values})
            print(result_tqc)

            render_mpl_table(result_tqc, header_columns=0, col_width=5.0)
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
            plt.savefig( root_path + 'TQC' + test_id + product_code  + 'Report.png')
            print(root_path + 'TQC' + test_id + product_code +  'Report.png' )
            status = True
        else:
            print("tqc找不到紀錄")

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return status 

def coil_pcm_report(coil_no):
    status = False
    try:
        df = db_pcmb030mPandas(coil_no)
#        for row in df['OPER_CODE']:
#            print(row)
        for index, row in df.iterrows():
            oper_code = row['OPER_CODE']
            new_station = OperCode_dic(oper_code)
            df.loc[index, 'OPER_CODE'] = new_station
            df.loc[index, 'COIL_THICK'] = round(row['COIL_THICK'],2)   
        if not df.empty:
            col_ren = { 
                        'COIL_NO':'產品編號','OPER_CODE':'產線','LAST_PROD_DATE':'產出日期','COIL_THICK':'厚度','COIL_WIDTH':'寬度', 
                        'COIL_WEIGHT':'重量','COIL_IN_DIAM':'內徑','COIL_OUT_DIAM':'外徑','IC_CODE':'鋼捲狀態','EDGING':'切邊',
                        'CLASS_CODE':'等級'
                      }
            df.rename(columns=col_ren, inplace=True) 
            print(df)
            render_mpl_table(df, header_columns=0)
            root_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "images") + "/"
            plt.savefig( root_path + 'PCM' + coil_no  + 'Report.png')
            print(root_path + 'PCM' + coil_no +  'Report.png' )
            status = True
        else:
            print("PCMB030M找不到紀錄")

    except Exception as e:
        print('Error: something worng, except message : ' + str(e))

    return status 
