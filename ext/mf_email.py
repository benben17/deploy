#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
This script used send email.
"""
import sys
import os
import smtplib
sys.path.append('..')
from email.mime.text import MIMEText
import ext.module as module


cf= module.get_config()


#设置服务器，用户名、口令以及邮箱的后缀
smtp_host=cf.get('smtp','smtp_host')
# smtp_host＝'smtp.163.com'
smtp_port=cf.get('smtp','smtp_port')
# mail_user="lizhenhua@mftour.cn"
mail_user=cf.get('smtp','smtp_user')
mail_pass=cf.get('smtp','smtp_pass')
mail_postfix=cf.get('smtp','mail_postfix')

# smtpObj=smtplib.SMTP()
# smtpObj.connect(smtp_host,smtp_port)
# smtpObj.login(mail_user, mail_pass)



#定义send_mail函数
def send_mail(to_list,sub,content):
    '''
    to_list:发给谁
    sub:主题
    content:内容
    send_mail("892100089@qq.com","sub","content")
    '''
    address="<"+mail_user+">"
    # +"<"+mail_user+"@"+mail_postfix+">"
    msg = MIMEText(content)
    msg['Subject']  =   sub
    msg['From']     =   address
    msg['To']       =   to_list
    try:
        s = smtplib.SMTP_SSL()
        # s.set_debuglevel(1)
        s.connect(smtp_host,smtp_port)
        s.login(mail_user,mail_pass)
        s.sendmail(address, to_list, msg.as_string())
        s.close()
        return True
    except Exception, e:
        print str(e)
        return False
if __name__ == '__main__':
    # send_mail(sys.argv[1], sys.argv[2], sys.argv[3])
    send_mail('892100089@qq.com', 'aa', 'ceshiceshiceshi')

# send_mail('892100089@qq.com', 'aa', 'ceshiceshiceshi')