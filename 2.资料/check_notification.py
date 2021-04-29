#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return yesterday


def mail_alert(message):
    """

    :type message: list
    """

    mail_host = "smtp.126.com"
    mail_user = "skiinder@126.com"
    mail_pass = "KADEMQZWCPFWZETF"

    sender = mail_user
    receivers = [mail_user]

    mail_content = MIMEText(''.join(['<html>', '<br>'.join(message), '</html>']), 'html', 'utf-8')
    mail_content['from'] = sender
    mail_content['to'] = receivers[0]
    mail_content['Subject'] = Header('数据监控错误', 'utf-8')

    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect(mail_host, 465)
        smtp.login(mail_user, mail_pass)
        content_as_string = mail_content.as_string()
        smtp.sendmail(sender, receivers, content_as_string)
    except smtplib.SMTPException as e:
        print e


def read_table(table, dt):
    mysql_user = "root"
    mysql_password = "000000"
    mysql_host = "hadoop102"
    mysql_schema = "test"

    # 从mysql中取数据并转化为字典
    connect = mysql.connector.connect(user=mysql_user, password=mysql_password, host=mysql_host, database=mysql_schema)
    cursor = connect.cursor()
    query = "desc " + table
    cursor.execute(query)
    head = map(lambda x: x[0], cursor.fetchall())
    query = ("select * from " + table + " where dt='" + dt + "' and `value` not between value_min and value_max")
    cursor.execute(query)
    fetchall = map(lambda x: dict(x), map(lambda x: zip(head, x), cursor.fetchall()))
    print type(fetchall[0])
    return fetchall


def main(argv):
    # 如果没有传入日期参数，将日期定为昨天
    if len(argv) >= 2:
        dt = argv[1]
    else:
        dt = str(get_yesterday())

    # 初始化警告正文
    alert_string = []

    # 如果警告数量大于0，发送警告
    if len(alert_string) > 0:
        mail_alert(alert_string)


if __name__ == "__main__":
    read_table("null_id", "2021-04-29")
    # main(sys.argv)
