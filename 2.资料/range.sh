#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# 检查di为空，参数说明如下：
# -t 表名
# -d 日期
# -c 列名
# -s 指标下限
# -x 指标上限
# -l 告警级别
# -a 值域上限
# -b 值域下限

while getopts "t:d:l:c:s:x:a:b:" arg; do
  case $arg in
  t)
    TABLE=$OPTARG
    ;;
  d)
    DT=$OPTARG
    ;;
  c)
    COL=$OPTARG
    ;;
  s)
    MIN=$OPTARG
    ;;
  x)
    MAX=$OPTARG
    ;;
  l)
    LEVEL=$OPTARG
    ;;
  a)
    RANGE_MIN=$OPTARG
    ;;
  b)
    RANGE_MAX=$OPTARG
    ;;
  ?)
    echo "unkonw argument"
    exit 1
    ;;
  esac
done

[ $DT ] || DT=$(date -d '-1 day' +%F)
[ $LEVEL ] || LEVEL=0

HIVE_DB=gmall
HIVE_ENGINE=hive
mysql_user="root"
mysql_passwd="000000"
mysql_host="hadoop102"
mysql_DB="test"
mysql_tbl="rng"

RESULT=$($HIVE_ENGINE -e "select count(1) from $HIVE_DB.$TABLE where dt='$DT' and $COL not between $RANGE_MIN and $RANGE_MAX;")
mysql -h"$mysql_host" -u"$mysql_user" -p"$mysql_passwd" \
  -e"INSERT INTO $mysql_DB.$mysql_tbl VALUES('$DT', '$TABLE', '$COL', $RESULT, $RANGE_MIN, $RANGE_MAX, $MIN, $MAX, $LEVEL)
ON DUPLICATE KEY UPDATE \`value\`=$RESULT, range_min=$RANGE_MIN, range_max=$RANGE_MAX, value_min=$MIN, value_max=$MAX, notification_level=$LEVEL;"
