#!/usr/bin/env bash
DT=$1
[ -z $DT ] || DT=$(date -d '-1 day' +%F)

bash day_on_day.sh -t ods_order_refund_info -d "$DT" -s -10 -x 10
bash week_on_week.sh -t ods_order_refund_info -d "$DT" -s -10 -x 50