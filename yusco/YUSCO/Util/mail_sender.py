# -*- coding: utf-8 -*-
"""
自動寄信
讀取excel文件後，根據工號自動發送
"""
import smtplib
import datetime
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication

def SEND_MAIL(arg_recipient, arg_subject, arg_msg, arg_msg_type):
	rt_code = 0

	#取得郵件發送系統參數
	sender_host = '100.1.1.5'
	sender_port = '25'
	sender_mail = 'ecmail@mail.yusco.com.tw'
	sender_id = 'yusco\\ecmail'
	sender_pwd = '!ecyucrmdmc'

	rt_desc = ""
	if len(arg_recipient) == 0:
		rt_code = 1
		rt_desc = "缺少收件者MAIL參數."

	if len(arg_subject) == 0:
		arg_subject = "無主旨"

	if len(arg_msg) == 0:
		arg_msg = " "

	if len(arg_msg_type) == 0:
		arg_msg_type = "plain"

	if rt_code == 0:

		curr_dt = datetime.datetime.now().strftime("%Y/%m/%d %H:%M:%S")
		recipient = arg_recipient
		
		msg = MIMEMultipart()
		

		msg['Subject'] = arg_subject
		msg['From'] = sender_mail
		msg['To'] = recipient
		msg.attach(MIMEText(arg_msg, arg_msg_type))

		xlsx = MIMEApplication(open('冷軋運轉日報表.xlsx', 'rb').read())
		xlsx["Content-Type"] = 'application/octet-stream'
		xlsx.add_header('Content-Disposition', 'attachment',
		                filename=('gbk', '', '冷軋運轉日報表.xlsx'))
		msg.attach(xlsx)

		xlsx = MIMEApplication(open('應用程式權限申請表說明.doc', 'rb').read())
		xlsx["Content-Type"] = 'application/octet-stream'
		xlsx.add_header('Content-Disposition', 'attachment',
		                filename=('gbk', '', '應用程式權限申請表說明.doc'))
		msg.attach(xlsx)
		

		try:
			server = smtplib.SMTP(sender_host, sender_port)
			server.ehlo()
			server.login(sender_id, sender_pwd)
			server.send_message(msg)
			server.quit()
			print(curr_dt + ' Email sent.')
		except Exception as e:
			rt_code = 5
			print(str(e))
			print("Err exception from MAIL_SENDER")
			print(str(e.args[0]))
			f = open("MAIL_SENDER_LOG.txt", "a")
			f.write("MAIL_SENDER Err:\n" + curr_dt + "\n" + str(e.args) + "\n\n")
			f.close()
			print('The mail not sent.')

	return rt_code, rt_desc

if __name__ == '__main__':
	print('請勿直接執行本程式...')	
