# -*- coding: utf-8 -*-
"""
爬蟲自動確認電子表單內容物
1.自動填寫程式代碼、程式名稱，並確認
2.儲存至json檔
"""
import re
from datetime import datetime, timedelta
import time
import pandas as pd
from openpyxl import load_workbook
import pyodbc
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.ie.options import Options
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


def writedown(driver, 電子表單個別項目_TR):
    """
    自動填入程式名稱及程式代碼
    """
    prog_no = re.compile(r'[A-Z]+[0-9]{3}')
    運轉日報表 = re.compile(r'[.+權限等級.+]|[.+運轉日報表.+]')
    prog_name = re.compile(
        r'[\u4e00-\u9fa5]+.+[\u4e00-\u9fa5]+|[\u4e00-\u9fa5]+|[A-Z]+[0-9]+[\u4e00-\u9fa5]+|[A-Z]+[\u4e00-\u9fa5]+|[\u4e00-\u9fa5]+')
    driver_wait = WebDriverWait(driver, 10)
    dsn_str = 'DRIVER={SQL Server};SERVER=100.1.1.25;DATABASE=PER;UID=sqluser;PWD=sqluser'
    處理說明 = driver_wait.until(
        EC.presence_of_element_located((By.ID, 'oxa38a010')))
    for adx, temp in enumerate(電子表單個別項目_TR):
        電子表單個別項目_TR_個別項目 = 電子表單個別項目_TR[adx].find_all('td')
        程式名稱 = 電子表單個別項目_TR_個別項目[4].text.strip()
        if (電子表單個別項目_TR_個別項目[10].text.strip()) == '':
            try:
                input_progno = re.findall(prog_no, 程式名稱)[0]
            except:
                conn = pyodbc.connect(dsn_str)
                strsql = "select prgno from secprg where prgname='"+程式名稱+"'"
                cursor = conn.cursor()
                cursor.execute(strsql)
                input_progno = cursor.fetchone()
                if input_progno is None:
                    input_progno = ''
                conn.close
            if (input_progno == '') & (len(re.findall(運轉日報表, 程式名稱)) > 0):
                input_progno = 'CRMRUN'
            程式代碼 = driver_wait.until(
                EC.presence_of_element_located((By.ID, 'txtPrgid'+str(adx))))
            程式代碼.send_keys(input_progno)
            處理說明.click()
            time.sleep(0.3)
        if (電子表單個別項目_TR_個別項目[11].text.strip()) == '':
            try:
                input_progname = re.findall(prog_name, 程式名稱)[0]
                print(input_progname)
            except:
                conn = pyodbc.connect(dsn_str)
                strsql = "select prgname from secprg where prgno='"+程式名稱+"'"
                print(strsql)
                cursor = conn.cursor()
                cursor.execute(strsql)
                input_progname = cursor.fetchone()
                if input_progname is None:
                    input_progname = ''
                conn.close
            if (input_progname == '') & (len(re.findall(運轉日報表, 程式名稱)) > 0):
                input_progname = '運轉日報表'
            程式名稱 = driver_wait.until(EC.presence_of_element_located(
                (By.ID, 'txtPrgname'+str(adx))))
            程式名稱.send_keys(input_progname)
            程式名稱.send_keys(Keys.ENTER)
            處理說明.click()
            time.sleep(0.3)
    處理說明.send_keys('准')
    """
    點選左上角的勾勾
    """
    driver.switch_to.default_content()
    driver.switch_to.frame("main")
    driver.switch_to.frame("Form_Func")  # 切換到溝溝的frame
    driver.find_element_by_id('btnYes').click()  # 點選勾勾
    driver.switch_to_alert().accept()  # 將js跳出來的alert點掉
    driver.switch_to.default_content()
    driver.switch_to.frame("main")
    try:
        driver.switch_to.frame("fraFormBody")
    except Exception as ex:
        print('在writedown結束', ex)


def switch_csv_down(every_td):
    # 將DICT轉成PANDAS並寫入CSV
    df = pd.DataFrame(every_td)
    try:
        df.to_csv('測試.csv', encoding='big5', header=None, mode='a')
    except:
        df.to_csv('測試.csv', encoding='utf-8', header=None, mode='a')
    print(every_td['No.0'][0]+'寫入完成')


def creep_ef2kweb(driver):
    # 爬取申請單內容
    fraFormBody = BeautifulSoup(driver.page_source, 'lxml')
    電子表單個別項目_TBODY = fraFormBody.find('tbody')
    電子表單個別項目_TR = 電子表單個別項目_TBODY.find_all(
        "tr", attrs={'style': 'FONT-SIZE: 14px; COLOR: #666666'})
    every_td = {}
    for awp, temp in enumerate(電子表單個別項目_TR):
        電子表單個別項目_TR_個別項目 = 電子表單個別項目_TR[awp].find_all('td')
        for adx, 個別項目_TD in enumerate(電子表單個別項目_TR_個別項目):
            if (個別項目_TD.div.text) != u'\xa0':
                every_td.setdefault(
                    'No.'+str(adx), []).append(個別項目_TD.div.text.replace(u'\xa0', u''))
            if (adx >= 5):
                try:
                    del every_td['No.'+str(adx)]
                except:
                    break
    switch_csv_down(every_td)
    writedown(driver, 電子表單個別項目_TR)


def main():
    # IE電子表單
    opts = Options()
    opts.ignore_protected_mode_settings = True
    opts.ignore_zoom_level = True
    opts.require_window_focus = True

    url = "http://100.1.1.23/ef2kweb/login.htm"
    driver = webdriver.Ie(ie_options=opts)
    driver.get(url)

    password = driver.find_element_by_id("text2")
    password.send_keys('ancx8888')
    time.sleep(3)
    user = driver.find_element_by_id("text1")
    user.send_keys(65426)
    time.sleep(3)
    try:
        password.send_keys(Keys.RETURN)
        time.sleep(3)
        driver.switch_to.frame("module")  # 切換id='module'的frame
    except:
        print('出錯')
        driver.quit()
    driver.find_element_by_id('FormData').click()  # 表單追蹤處理
    driver.find_element_by_id('imgHandle1').click()  # 收件夾
    driver.switch_to.default_content()  # 切換到主文檔
    driver.switch_to.frame("main")  # 切換到id='main'的frame
    test = driver.find_elements_by_tag_name('tr')[3]  # 收件夾
    test.click()
    driver.switch_to.frame("fraFormBody")

    while driver:
        creep_ef2kweb(driver)
    else:
        print('結束')
        exit()


if __name__ == "__main__":
    main()
