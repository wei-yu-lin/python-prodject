# -*- coding: utf-8 -*-
"""
EC製程管制網資料爬取公用程式

說明:
    1. class YuProcControl: 產線參數類別，與公用function

    2. def ie_get_yusco_ec_web: 各產線製程管制數據抓取(使用IE)

    3. def MV_YuProcControlFile: 搬移 XXXX_PROC_CONTROL_DATA_YYYYMMDD.xlsx 檔案至共享目錄

"""
import json
import os
import re
import time
from shutil import move

import pandas as pd
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.options import Options


class YuProcControl:
    def __init__(self, arg_file_name):
        self.pl_dict = json.load(open(arg_file_name + ".json",encoding="utf-8"))

    def get_pl_dict(self, param):
        rt_parm = self.pl_dict.get(param,'')
        return rt_parm
    
    def pl_dict_list(self):
        ls = []
        for key in self.pl_dict:
            ls.append(key)
        
        return ls

def ie_get_yusco_ec_web(arg_pl_dict, arg_url, arg_type='A'):
    #設定忽略IE Zoom Level
    opts = Options()
    opts.ignore_protected_mode_settings = True
    opts.ignore_zoom_level = True
    opts.require_window_focus = True

    while True:
        driver = webdriver.Ie(ie_options=opts)
        driver.get(arg_pl_dict['m_link'])
        print(arg_url)
        driver.get(arg_url)
        soup_level2=BeautifulSoup(driver.page_source, 'lxml')     
        
        driver.quit()  #關閉IE
        
        #判斷是否因session過期，無法讀取到網頁資料，重新get網頁
        table = soup_level2.find_all('table')[0]
        if table.text.find('伺服主機許未得到您的回應,為確認身份請重新登入系統') == -1:
            break
        else:
            print("網頁session過期，重新讀取網頁.")

    table = soup_level2.find_all('table', attrs={'id':'tb_data'})
    
    if len(table) > 0:
        rows = table[0].find_all('tr')
        data = []
        for row in rows:
            data.append([ele.text for ele in row.find_all('td')])
        print("剛抓取下來的td=",data,'/n')
        #df = pd.DataFrame(data[1:-2], columns=data[0])
        df = pd.DataFrame(data[1:], columns=data[0])
        print("df=",df)
        
    else:
        df = pd.DataFrame()

    detail_ls = []
    if arg_type == 'B':
        p = re.compile(r"'([\S\s]*)'")
        for item in soup_level2.find_all('td', onclick = re.compile(r"fun_Pass_data")): #soup.find_all返回的为列表
            #print(item.get('onclick'))
            grp = p.findall(item.get('onclick'))
            detail_ls.append(str(grp[0]).replace(" ", "").replace("'", "").split(","))
            #print(str(grp[0]).replace(" ", "").replace("'", "").split(","))

    return df, detail_ls


def MV_YuProcControlFile(arg_des_path=''):
    print("搬移 XXXX_PROC_CONTROL_DATA_YYYYMMDD.xlsx 檔案...")
    cwd = os.getcwd()
    file_ls = []
    for file in os.listdir(cwd):
        if file.endswith("APL1-4_PROC_CONTROL_DATA.xlsx") or file.endswith("CRM1-6_PROC_CONTROL_DATA.xlsx") or file.endswith("HSM_PROC_CONTROL_DATA.xlsx"):
           #print(file)
           file_ls.append(file)

    #print(file_ls)

    for mv_file in file_ls:
        tar_file = cwd + "\\" + mv_file
        des_file = arg_des_path + mv_file

        try:
            move(tar_file, des_file)
            print(mv_file + "移動檔案完畢.")
        except Exception as e:
            print(mv_file + "移動檔案失敗.")
            print(e.args)

    print("搬移檔案結束...")
