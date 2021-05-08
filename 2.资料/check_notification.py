#!/usr/bin/env python
# -*- coding: utf-8 -*-

import mysql.connector
import sys
import smtplib
from email.mime.text import MIMEText
from email.header import Header
import datetime
import urllib
import urllib2
import random


def get_yesterday():
    today = datetime.date.today()
    one_day = datetime.timedelta(days=1)
    yesterday = today - one_day
    return str(yesterday)


def one_alert(line):
    """

    :type line: dict
    """

    # 睿象云的rest api key
    one_alert_key = "c2030c9a-7896-426f-bd64-59a8889ac8e3"
    one_alert_host = "http://api.aiops.com/alert/api/event"

    data = {
        "app": one_alert_key,
        "eventType": "trigger",
        "eventId": str(random.randint(10000, 99999)),
        "alarmName": "".join(["表格", str(line["tbl"]), "数据异常."]),
        "alarmContent": "".join(["指标", str(line["norm"]), "值为", str(line["value"]),
                                 ", 应为", str(line["value_min"]), "-", str(line["value_max"]),
                                 ", 参考信息：" + str(line["col"]) if line.get("col") else ""]),
        "priority": line["notification_level"] + 1
    }

    body = urllib.urlencode(data)
    request = urllib2.Request(one_alert_host, body)
    urlopen = urllib2.urlopen(request).read().decode('utf-8')
    print urlopen


def mail_alert(line):
    """

    :type line: dict
    """

    # smtp协议发送邮件的必要设置
    mail_host = "smtp.126.com"
    mail_user = "skiinder@126.com"
    mail_pass = "KADEMQZWCPFWZETF"

    message = ["".join(["表格", str(line["tbl"]), "数据异常."]),
               "".join(["指标", str(line["norm"]), "值为", str(line["value"]),
                        ", 应为", str(line["value_min"]), "-", str(line["value_max"]),
                        ", 参考信息：" + str(line["col"]) if line.get("col") else ""])]

    sender = mail_user
    receivers = [mail_user]

    mail_content = MIMEText("".join(["<html>", "<br>".join(message), "</html>"]), "html", "utf-8")
    mail_content["from"] = sender
    mail_content["to"] = receivers[0]
    mail_content["Subject"] = Header(message[0], "utf-8")

    try:
        smtp = smtplib.SMTP_SSL()
        smtp.connect(mail_host, 465)
        smtp.login(mail_user, mail_pass)
        content_as_string = mail_content.as_string()
        smtp.sendmail(sender, receivers, content_as_string)
    except smtplib.SMTPException as e:
        print e


def read_table(table, dt):

    # mysql必要参数设置
    mysql_user = "root"
    mysql_password = "000000"
    mysql_host = "hadoop102"
    mysql_schema = "test"

    # 从mysql中取数据并转化为字典
    connect = mysql.connector.connect(user=mysql_user, password=mysql_password, host=mysql_host, database=mysql_schema)
    cursor = connect.cursor()
    query = "desc " + table
    cursor.execute(query)
    head = map(lambda x: str(x[0]), cursor.fetchall())
    query = ("select * from " + table + " where dt='" + dt + "' and `value` not between value_min and value_max")
    cursor.execute(query)
    cursor_fetchall = cursor.fetchall()
    fetchall = map(lambda x: dict(x), map(lambda x: zip(head, x), cursor_fetchall))
    return fetchall


def main(argv):
    # 如果没有传入日期参数，将日期定为昨天
    if len(argv) >= 3:
        dt = argv[2]
    else:
        dt = get_yesterday()

    notification_level = 0

    alert = None
    if len(argv) >= 2:
        alert = {
            "mail": mail_alert,
            "one": one_alert
        }[argv[1]]
    if not alert:
        alert = one_alert

    # 查询所有错误内容，如果大于设定警告等级，就发送警告
    for table in ["day_on_day", "duplicate", "null_id", "rng", "std_dev", "week_on_week"]:
        for line in read_table(table, dt):
            if line["notification_level"] >= notification_level:
                line["norm"] = table
                alert(line)


if __name__ == "__main__":
    # 两个命令行参数
    # 第一个为警告类型：one或者mail
    # 第二个为日期，留空取昨天
    main(sys.argv)
