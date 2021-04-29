#!/usr/bin/env bash
# -*- coding: utf-8 -*-
# 检查di为空，参数说明如下：
# -t 表名
# -d 日期
# -c 列名
# -s 指标下限
# -x 指标上限
# -l 告警级别

while getopts "t:d:s:x:l:" arg; do
  case $arg in
  t)
    TABLE=$OPTARG
    ;;
  d)
    DT=$OPTARG
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
mysql_tbl="week_on_week"

LASTWEEK=$($HIVE_ENGINE -e "select count(1) from $HIVE_DB.$TABLE where dt between date_add('$DT',-13) and date_add('$DT',-7);")
THISWEEK=$($HIVE_ENGINE -e "select count(1) from $HIVE_DB.$TABLE where dt between date_add('$DT',-6) and '$DT';")
if [ $LASTWEEK -ne 0 ]; then
  RESULT=$(awk "BEGIN{print ($THISWEEK-$LASTWEEK)/$LASTWEEK*100}")
else
  RESULT=10000
fi
mysql -h"$mysql_host" -u"$mysql_user" -p"$mysql_passwd" \
  -e"INSERT INTO $mysql_DB.$mysql_tbl VALUES('$DT', '$TABLE', $RESULT, $MIN, $MAX, $LEVEL)
ON DUPLICATE KEY UPDATE \`value\`=$RESULT, value_min=$MIN, value_max=$MAX, notification_level=$LEVEL;"
