#!/usr/bin/env python
# -*- coding: utf-8 -*-
from pyhive import hive
from mysql import connector as mysql
import getopt, sys

# hive必要参数设置
hive_user = "atguigu"
hive_host = "hadoop102"

# mysql必要参数设置
mysql_user = "root"
mysql_password = "000000"
mysql_host = "hadoop102"


def query(engine, sql):
    if engine == "mysql":
        connect = mysql.connect(host=mysql_host, password=mysql_password, user=mysql_user)
    else:
        connect = hive.connect(host=hive_host, username=hive_user)

    cursor = connect.cursor()
    cursor.execute(sql)
    fetchall = cursor.fetchall()
    cursor.close()
    connect.close()
    return fetchall


if __name__ == '__main__':
    print dict(getopt.getopt(sys.argv[1:], "t:d:c:s:x:l:")[0])
